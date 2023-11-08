import json
import math
import os
import time
from concurrent import futures
from dataclasses import dataclass

import grpc

from proto import geo_pb2, geo_pb2_grpc

GEO_SERVICE_ADDRESS = '[::]:8080'
EARTH_RADIUS_KM = 6371.0
MAX_SEARCH_RADIUS_KM = 10  # limit to 10 km

current_dir = os.path.dirname(os.path.abspath(__file__))
json_filepath = os.path.join(current_dir, '..', 'data', 'geo.json')


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

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = math.sin(dlat / 2) * math.sin(dlat / 2) + math.cos(math.radians(lat1)) * math.cos(
        math.radians(lat2)) * math.sin(dlon / 2) * math.sin(dlon / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return EARTH_RADIUS_KM * c


def find_nearby_hotels(hotels, point, radius):
    nearby_hotels = []

    for hotel in hotels:
        hotel_coord = (hotel['lat'], hotel['lon'])
        distance = haversine_distance(point, hotel_coord)

        if distance <= radius:
            nearby_hotels.append(hotel['hotelId'])

    return nearby_hotels


class GeoServicer(geo_pb2_grpc.GeoServicer):
    def Nearby(self, request, context):
        point = (request.lat, request.lon)
        hotels = load_hotels(json_filepath)
        hotel_ids = find_nearby_hotels(hotels, point, MAX_SEARCH_RADIUS_KM)
        return geo_pb2.Result(hotelIds=hotel_ids)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    geo_pb2_grpc.add_GeoServicer_to_server(GeoServicer(), server)
    server.add_insecure_port(GEO_SERVICE_ADDRESS)
    server.start()
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)
