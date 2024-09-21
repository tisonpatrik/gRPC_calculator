import grpc
from fastapi import APIRouter, Depends, HTTPException, status

from calculator.src.pb import add_pb2, add_pb2_grpc
from calculator.src.validations.requests import AddRequest

router = APIRouter()


@router.get(
    "/add/",
    status_code=status.HTTP_200_OK,
    name="Add",
)
def add_endpoint(
    query: AddRequest = Depends(),
):
    # Připojení ke gRPC serveru pomocí hostname kontejneru (add)
    with grpc.insecure_channel("add:50051") as channel:
        stub = add_pb2_grpc.AddServiceStub(channel)

        grpc_request = add_pb2.AddRequest(x=query.x, y=query.y)

        try:
            # Volání gRPC metody Add a získání odpovědi
            response = stub.Add(grpc_request)
        except grpc.RpcError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
            )

    # Vracení výsledku jako odpověď FastAPI
    return {"result": response.result}
