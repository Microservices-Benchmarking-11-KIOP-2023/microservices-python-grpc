import grpc

import search_pb2
import search_pb2_grpc


def run():
    channel = grpc.insecure_channel('localhost:50051')
    stub = search_pb2_grpc.SearchStub(channel)

    request = search_pb2.NearbyRequest(
        lat=37.7000,
        lon=-122.4112,
        inDate="2014-10-28",
        outDate="2014-11-01"
    )

    response = stub.Nearby(request)

    for hotel_id in response.hotelIds:
        print(f"Hotel ID: {hotel_id}")


if __name__ == '__main__':
    run()
