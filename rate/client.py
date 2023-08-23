import grpc
import rate_pb2
import rate_pb2_grpc


def run():
    # Step 2: Create a channel
    channel = grpc.insecure_channel('localhost:50051')

    # Step 3: Create a stub
    stub = rate_pb2_grpc.RateStub(channel)

    # Step 4: Build the request
    request = rate_pb2.Request(
        hotelIds=['1', '2'],
        inDate='2014-03-17',
        outDate='2014-03-21'
    )

    # Step 5: Call the service method
    response = stub.GetRates(request)

    # Step 6: Process the response
    print("Client received response:\n")
    for ratePlan in response.ratePlans:
        print(f"Hotel ID: {ratePlan.hotelId}")
        print(f"Rate Code: {ratePlan.code}")
        print(f"Check-in Date: {ratePlan.inDate}")
        print(f"Check-out Date: {ratePlan.outDate}")
        print("Room Type:")
        print(f"  Bookable Rate: {ratePlan.roomType.bookableRate}")
        print(f"  Total Rate: {ratePlan.roomType.totalRate}")
        print(f"  Total Rate Inclusive: {ratePlan.roomType.totalRateInclusive}")
        print(f"  Room Code: {ratePlan.roomType.code}")
        print(f"  Currency: {ratePlan.roomType.currency}")
        print(f"  Room Description: {ratePlan.roomType.roomDescription}")
        print("\n")


if __name__ == '__main__':
    run()
