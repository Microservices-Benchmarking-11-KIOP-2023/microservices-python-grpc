import time
from concurrent import futures

import grpc

from services.geo.proto import geo_pb2, geo_pb2_grpc
from services.rate.proto import rate_pb2, rate_pb2_grpc
from services.search.proto import search_pb2, search_pb2_grpc


class SearchServicer(search_pb2_grpc.SearchServicer):
    def Nearby(self, request, context):
        geo_channel = grpc.insecure_channel('localhost:5003')
        geo_stub = geo_pb2_grpc.GeoStub(geo_channel)
        location_request = geo_pb2.Request(lat=request.lat, lon=request.lon)
        geo_response = geo_stub.Nearby(location_request)

        rate_channel = grpc.insecure_channel('localhost:5004')
        rate_stub = rate_pb2_grpc.RateStub(rate_channel)
        rate_request = rate_pb2.Request(hotelIds=geo_response.hotelIds, inDate=request.inDate, outDate=request.outDate)
        rate_response = rate_stub.GetRates(rate_request)

        available_hotel_ids = [rate_plan.hotelId for rate_plan in rate_response.ratePlans]

        return search_pb2.SearchResult(hotelIds=available_hotel_ids)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    search_pb2_grpc.add_SearchServicer_to_server(SearchServicer(), server)
    server.add_insecure_port('localhost:5001')
    server.start()
    try:
        while True:
            time.sleep(86400)  # One day in seconds
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()



