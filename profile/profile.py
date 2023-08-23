import grpc
from concurrent import futures
import time
import profile_pb2
import profile_pb2_grpc
import json


def load_profiles(hotel_ids, file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        return "The file was not found."
    except json.JSONDecodeError:
        return "Error parsing the JSON file."

    matching_profiles = [hotel_profile for hotel_profile in data if hotel_profile['id'] in hotel_ids]
    return matching_profiles if matching_profiles else None


file_path = '../data/hotels.json'

class ProfileServicer(profile_pb2_grpc.ProfileServicer):
    def GetProfiles(self, request, context):
        hotel_profiles = load_profiles(request.hotelIds, file_path)
        if hotel_profiles is None:
            return profile_pb2.Result()
        else:
            result = profile_pb2.Result()
            for profile in hotel_profiles:
                hotel = result.hotels.add()
                hotel.id = profile['id']
                hotel.name = profile['name']
                hotel.phoneNumber = profile['phoneNumber']
                hotel.description = profile['description']

                address = profile['address']
                hotel.address.streetNumber = address['streetNumber']
                hotel.address.streetName = address['streetName']
                hotel.address.city = address['city']
                hotel.address.state = address['state']
                hotel.address.country = address['country']
                hotel.address.postalCode = address['postalCode']
                hotel.address.lat = address['lat']
                hotel.address.lon = address['lon']
        return result


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    profile_pb2_grpc.add_ProfileServicer_to_server(ProfileServicer(), server)
    server.add_insecure_port('localhost:5002')
    server.start()
    try:
        while True:
            time.sleep(86400)  # One day in seconds
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()



