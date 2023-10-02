import grpc
from flask import Flask, request, jsonify

from services.profile.proto import profile_pb2, profile_pb2_grpc
from services.search.proto import search_pb2, search_pb2_grpc

app = Flask(__name__)

SEARCH_SERVICE_ADDRESS = 'localhost:5001'
PROFILE_SERVICE_ADDRESS = 'localhost:5002'


@app.route('/hotels', methods=['GET'])
def get_hotels():
    # Parse the HTTP request
    in_date = request.args.get('inDate')
    out_date = request.args.get('outDate')
    lat = float(request.args.get('lat'))
    lon = float(request.args.get('lon'))

    # Call the search service using gRPC
    with grpc.insecure_channel(SEARCH_SERVICE_ADDRESS) as channel:
        stub = search_pb2_grpc.SearchStub(channel)
        response = stub.Nearby(search_pb2.NearbyRequest(lat=lat, lon=lon, inDate=in_date, outDate=out_date))

    hotel_ids = response.hotelIds

    # Call the profile service using gRPC
    with grpc.insecure_channel(PROFILE_SERVICE_ADDRESS) as channel:
        stub = profile_pb2_grpc.ProfileStub(channel)
        response = stub.GetProfiles(profile_pb2.Request(hotelIds=hotel_ids))

    # Convert the gRPC response to a JSON-friendly format
    hotels = [{'id': hotel.id, 'coordinates': {'lat': hotel.address.lat, 'lon': hotel.address.lon},
               'properties': {'name': hotel.name, 'phone_number': hotel.phoneNumber}} for hotel in response.hotels]
    return jsonify(hotels)


if __name__ == "__main__":
    app.run(port=5000)
