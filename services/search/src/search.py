import time
from concurrent import futures

import grpc

from proto import geo_pb2, geo_pb2_grpc
from proto import rate_pb2, rate_pb2_grpc
from proto import search_pb2, search_pb2_grpc

SEARCH_SERVICE_ADDRESS = '[::]:8080'
GEO_SERVICE_ADDRESS = 'geo:8080'
RATE_SERVICE_ADDRESS = 'rate:8080'


class SearchServicer(search_pb2_grpc.SearchServicer):
    def Nearby(self, request, context):
        import time
        start_time = time.time()
        geo_channel = grpc.insecure_channel(GEO_SERVICE_ADDRESS)
        geo_stub = geo_pb2_grpc.GeoStub(geo_channel)
        location_request = geo_pb2.Request(lat=request.lat, lon=request.lon)
        geo_response = geo_stub.Nearby(location_request)
        end_time = time.time()
        print(f"Time taken in search service, geo call: {end_time - start_time} seconds")

        start_time = time.time()
        rate_channel = grpc.insecure_channel(RATE_SERVICE_ADDRESS)
        rate_stub = rate_pb2_grpc.RateStub(rate_channel)
        rate_request = rate_pb2.Request(hotelIds=geo_response.hotelIds, inDate=request.inDate, outDate=request.outDate)
        rate_response = rate_stub.GetRates(rate_request)
        end_time = time.time()
        print(f"Time taken in search service, rate call: {end_time - start_time} seconds")

        available_hotel_ids = [rate_plan.hotelId for rate_plan in rate_response.ratePlans]


        return search_pb2.SearchResult(hotelIds=available_hotel_ids)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    search_pb2_grpc.add_SearchServicer_to_server(SearchServicer(), server)
    server.add_insecure_port(SEARCH_SERVICE_ADDRESS)
    server.start()
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)
