import grpc
from concurrent import futures
import time
import geo_pb2
import geo_pb2_grpc
import json

import math

from dataclasses import dataclass

MAX_SEARCH_RADIUS_IN_KM = 10        # limit to 10 km

@dataclass
class Point:
    point_id: int
    point_latitude: int
    point_longitude: int


def load_hotels(json_filepath):
    with open(json_filepath, 'r') as file:
        hotels = json.load(file)
    return hotels


def haversine_distance(coord1, coord2):
    lat1, lon1 = coord1
    lat2, lon2 = coord2

    R = 6371.0  # Earth radius in kilometers

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = math.sin(dlat / 2) * math.sin(dlat / 2) + math.cos(math.radians(lat1)) * math.cos(
        math.radians(lat2)) * math.sin(dlon / 2) * math.sin(dlon / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c


def find_nearby_hotels(hotels, point, radius=10):
    nearby_hotels = []

    for hotel in hotels:
        hotel_coord = (hotel['lat'], hotel['lon'])
        distance = haversine_distance(point, hotel_coord)

        if distance <= radius:
            nearby_hotels.append(hotel['hotelId'])

    return nearby_hotels


json_filepath = '../data/geo.json'

hotels = load_hotels(json_filepath)


class GeoServicer(geo_pb2_grpc.GeoServicer):
    def Nearby(self, request, context):
        point = (request.lat, request.lon)
        hotel_ids = find_nearby_hotels(hotels, point, 10)
        return geo_pb2.Result(hotelIds=hotel_ids)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    geo_pb2_grpc.add_GeoServicer_to_server(GeoServicer(), server)
    server.add_insecure_port('localhost:5003')
    server.start()
    try:
        while True:
            time.sleep(86400)  # One day in seconds
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()
