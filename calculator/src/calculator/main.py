from datetime import datetime

import grpc
import httpx
import pandas as pd
import pyarrow as pa
from fastapi import APIRouter, FastAPI, HTTPException, status
from fastapi.responses import ORJSONResponse

from calculator.pb import time_series_pb2, time_series_pb2_grpc


def from_api_to_series(items: dict) -> pd.Series:
    columns = ["time", "price"]
    data = pd.DataFrame(list(items.items()))
    data.columns = columns
    data["time"] = pd.to_datetime(data["time"], errors="coerce").dt.strftime(
        "%Y-%m-%d %H:%M:%S"
    )
    sorted_data_frame = data.sort_values(by="time")
    series = pd.Series(
        sorted_data_frame["price"].values, index=sorted_data_frame["time"]
    )
    return series


# FastAPI app configurations
app_configs = {
    "title": "Calculator API",
    "description": "Service to provide calculations using gRPC and HTTP",
    "version": "0.1.0",
    "redirect_slashes": False,
    "default_response_class": ORJSONResponse,
}

# Initialize the FastAPI app
app = FastAPI(**app_configs)

# Create the API router
router = APIRouter()


@router.get(
    "/grpc_generate_time_series/",
    status_code=status.HTTP_200_OK,
    name="Generate Time Series via gRPC",
)
async def grpc_generate_time_series(length: int):
    """
    Endpoint to generate a time series using the gRPC service.
    """
    with grpc.insecure_channel("grpc_api:50051") as channel:
        start_time = datetime.now()
        stub = time_series_pb2_grpc.TimeSeriesServiceStub(channel)
        grpc_request = time_series_pb2.TimeSeriesRequest(length=length)

        # Make the gRPC call to generate the time series
        try:
            grpc_response = stub.GenerateTimeSeries(grpc_request)
        except grpc.RpcError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"gRPC error: {e.details()}",
            )

        # Deserialize the Arrow data into a Pandas DataFrame
        serialized_data = grpc_response.serialized_series
        buffer = pa.BufferReader(serialized_data)
        reader = pa.ipc.open_file(buffer)
        table = reader.read_all()
        df = table.to_pandas()

        # Convert DataFrame to a Pandas Series
        series = pd.Series(data=df["price"].values, index=pd.to_datetime(df["time"]))

    end_time = datetime.now()
    print(f"Time taken to generate time series via gRPC: {end_time - start_time}")
    return series.head()


@router.get(
    "/http_generate_time_series/",
    status_code=status.HTTP_200_OK,
    name="Generate Time Series via HTTP",
)
async def http_generate_time_series(length: int):
    """
    Endpoint to generate a time series by calling the REST API via HTTP.
    """
    api_url = "http://rest_api:8100/generate_time_series/"

    start_time = datetime.now()
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(api_url, params={"length": length})
            response.raise_for_status()
            data = response.json()
    except httpx.HTTPError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"HTTP error: {str(e)}",
        )

    # Create a Pandas DataFrame for the data
    series = from_api_to_series(data)
    end_time = datetime.now()
    print(f"Time taken to generate time series via http: {end_time - start_time}")
    return series.head()


# Include the router in the FastAPI app
app.include_router(router)
