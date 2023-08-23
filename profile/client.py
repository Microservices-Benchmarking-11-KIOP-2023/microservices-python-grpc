import grpc
import profile_pb2
import profile_pb2_grpc


def print_hotel(hotel):
    print('Hotel ID:', hotel.id)
    print('Name:', hotel.name)
    print('Phone Number:', hotel.phoneNumber)
    print('Description:', hotel.description)
    print('Address:', hotel.address.streetNumber, hotel.address.streetName,
          hotel.address.city, hotel.address.state, hotel.address.country,
          hotel.address.postalCode, hotel.address.lat, hotel.address.lon)
    for image in hotel.images:
        print('Image URL:', image.url, 'Default:', image.default)
    print()


def run():
    channel = grpc.insecure_channel('localhost:50051')
    stub = profile_pb2_grpc.ProfileStub(channel)

    request = profile_pb2.Request(
        hotelIds=["1", "3", "5"]
    )

    response = stub.GetProfiles(request)

    for hotel in response.hotels:
        print_hotel(hotel)


if __name__ == '__main__':
    run()
