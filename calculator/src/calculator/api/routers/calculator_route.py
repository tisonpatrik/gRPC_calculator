import grpc
from fastapi import APIRouter, HTTPException, status

from calculator.pb import time_series_pb2, time_series_pb2_grpc

router = APIRouter()


@router.get(
    "/generate_time_series/",
    status_code=status.HTTP_200_OK,
    name="Generate Time Series",
)
async def generate_time_series(length: int):
    with grpc.insecure_channel("grpc_api:50051") as channel:
        stub = time_series_pb2_grpc.TimeSeriesServiceStub(channel)
        grpc_request = time_series_pb2.TimeSeriesRequest(length=length)
        try:
            response = stub.GenerateTimeSeries(grpc_request)

            # Convert the series points to a list of dictionaries
            series_data = [
                {"time": point.time.ToDatetime().isoformat(), "price": point.price}
                for point in response.series.points
            ]

        except grpc.RpcError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
            )

    return {"series": series_data}
