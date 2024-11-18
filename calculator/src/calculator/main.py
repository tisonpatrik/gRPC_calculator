from datetime import datetime

import grpc
import httpx
import pandas as pd
from fastapi import APIRouter, FastAPI, HTTPException, status
from fastapi.responses import ORJSONResponse

from calculator.pb import time_series_pb2, time_series_pb2_grpc

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
        try:
            response = stub.GenerateTimeSeries(grpc_request)

            # Convert the series points to a list of dictionaries
            series_data = [
                {"time": point.time.ToDatetime().isoformat(), "price": point.price}
                for point in response.series.points
            ]

        except grpc.RpcError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"gRPC error: {str(e)}",
            )

    # Create a Pandas DataFrame for the data
    series = pd.DataFrame(series_data)
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
    series = pd.DataFrame(data)
    end_time = datetime.now()
    print(f"Time taken to generate time series via http: {end_time - start_time}")
    return series.head()


# Include the router in the FastAPI app
app.include_router(router)
