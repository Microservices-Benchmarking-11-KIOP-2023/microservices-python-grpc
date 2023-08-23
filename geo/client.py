import grpc
import geo_pb2
import geo_pb2_grpc


def run():
    channel = grpc.insecure_channel('localhost:50051')
    stub = geo_pb2_grpc.GeoStub(channel)

    request = geo_pb2.Request(
        lat=37.7000,
        lon=-122.4112
    )

    response = stub.Nearby(request)

    for hotel_id in response.hotelIds:
        print(f"Hotel ID: {hotel_id}")


if __name__ == '__main__':
    run()
