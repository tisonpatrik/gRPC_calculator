# grpc/src/grpc/main.py

import random
from concurrent import futures
from datetime import datetime, timedelta

import grpc
import pandas as pd

from grpc_api.pb.time_series_pb2 import Series, SeriesPoint, TimeSeriesResponse
from grpc_api.pb.time_series_pb2_grpc import (
    TimeSeriesServiceServicer,
    add_TimeSeriesServiceServicer_to_server,
)


class TimeSeriesService(TimeSeriesServiceServicer):
    def GenerateTimeSeries(self, request, context):
        # Generate a Pandas Series of the specified length
        length = request.length
        start_time = datetime.now()
        timestamps = [start_time + timedelta(minutes=i) for i in range(length)]
        prices = [random.uniform(10, 100) for _ in range(length)]  # Random prices

        pandas_series = pd.Series(data=prices, index=timestamps)

        # Convert Pandas Series to gRPC Series message
        series = Series()
        for timestamp, price in pandas_series.items():
            point = SeriesPoint()
            point.time.FromDatetime(timestamp)  # Ensure gRPC Timestamp compatibility
            point.price = price
            series.points.append(point)

        return TimeSeriesResponse(series=series)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_TimeSeriesServiceServicer_to_server(TimeSeriesService(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    print("Server started on port 50051.")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
