from add.src.pb import add_pb2 as add_service_pb2
from add.src.pb import add_pb2_grpc as add_service_pb2_grpc


# Třída AddServiceHandler, která implementuje gRPC metody
class AddService(add_service_pb2_grpc.AddServiceServicer):
    # Implementace metody Add
    def Add(self, request, context):
        # Sečtení dvou čísel z requestu
        result = request.x + request.y

        # Vracení odpovědi AddResponse s výsledkem
        return add_service_pb2.AddResponse(result=result)
