import json
import time
from concurrent import futures
from typing import List
import os

import grpc

from services.rate.proto import rate_pb2, rate_pb2_grpc

# Get the directory of the currently executing script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the full path to the geo.json file
json_filepath = os.path.join(current_dir, '..', '..', 'data', 'inventory.json')


class RoomType:
    def __init__(self, bookableRate, totalRate, totalRateInclusive, code, currency, roomDescription):
        self.bookableRate = bookableRate
        self.totalRate = totalRate
        self.totalRateInclusive = totalRateInclusive
        self.code = code
        self.currency = currency
        self.roomDescription = roomDescription


class RatePlan:
    def __init__(self, hotelId, code, inDate, outDate, roomType):
        self.hotelId = hotelId
        self.code = code
        self.inDate = inDate
        self.outDate = outDate
        self.roomType = roomType


class Result:
    def __init__(self, ratePlans: List[RatePlan]):
        self.ratePlans = ratePlans


def get_rates(hotelIds: List[str], inDate: str, outDate: str) -> Result:
    with open(json_filepath, 'r') as file:
        data = json.load(file)

    filtered_data = [rate for rate in data if
                     rate['hotelId'] in hotelIds and rate['inDate'] >= inDate and rate['outDate'] <= outDate]
    ratePlans = []
    for rate in filtered_data:
        roomType_data = rate['roomType']
        roomType = RoomType(
            bookableRate=roomType_data['bookableRate'],
            totalRate=roomType_data['totalRate'],
            totalRateInclusive=roomType_data['totalRateInclusive'],
            code=roomType_data['code'],
            currency=roomType_data.get('currency', 'USD'),
            roomDescription=roomType_data.get('description', '')
        )

        ratePlan = RatePlan(
            hotelId=rate['hotelId'],
            code=rate['code'],
            inDate=rate['inDate'],
            outDate=rate['outDate'],
            roomType=roomType
        )

        ratePlans.append(ratePlan)

    result = Result(ratePlans=ratePlans)
    return result

class RateServicer(rate_pb2_grpc.RateServicer):
    def GetRates(self, request, context):
        result = get_rates(request.hotelIds, request.inDate, request.outDate)

        response = rate_pb2.Result()
        for ratePlan in result.ratePlans:
            rate_plan_proto = response.ratePlans.add()
            rate_plan_proto.hotelId = ratePlan.hotelId
            rate_plan_proto.code = ratePlan.code
            rate_plan_proto.inDate = ratePlan.inDate
            rate_plan_proto.outDate = ratePlan.outDate

            room_type_proto = rate_plan_proto.roomType
            room_type_proto.bookableRate = ratePlan.roomType.bookableRate
            room_type_proto.totalRate = ratePlan.roomType.totalRate
            room_type_proto.totalRateInclusive = ratePlan.roomType.totalRateInclusive
            room_type_proto.code = ratePlan.roomType.code
            room_type_proto.currency = ratePlan.roomType.currency
            room_type_proto.roomDescription = ratePlan.roomType.roomDescription

        return response


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    rate_pb2_grpc.add_RateServicer_to_server(RateServicer(), server)
    server.add_insecure_port('localhost:5004')
    server.start()
    try:
        while True:
            time.sleep(86400)  # One day in seconds
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()