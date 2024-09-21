from concurrent import futures

import grpc

from add.src.pb import add_pb2_grpc as add_service_pb2_grpc
from add.src.services.add_service import AddService


# Funkce pro spuštění gRPC serveru
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    # Přidání AddServiceHandler do serveru
    add_service_pb2_grpc.add_AddServiceServicer_to_server(AddService(), server)

    # Server bude naslouchat na portu 50051
    server.add_insecure_port("[::]:50051")
    print("gRPC server running on port 50051")

    # Spuštění serveru
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
