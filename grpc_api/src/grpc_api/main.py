from datetime import datetime, timedelta

import grpc
import numpy as np
import pandas as pd
import pyarrow as pa

from grpc_api.pb import time_series_pb2, time_series_pb2_grpc


class TimeSeriesService(time_series_pb2_grpc.TimeSeriesServiceServicer):
    async def GenerateTimeSeries(self, request, context):
        """
        Generate a time series of the specified length using Apache Arrow for serialization.
        """
        length = request.length
        start_time = datetime.now()

        # Generate timestamps and random prices
        timestamps = [start_time + timedelta(minutes=i) for i in range(length)]
        prices = np.random.uniform(10, 100, size=length)

        # Create a Pandas DataFrame
        df = pd.DataFrame({"time": timestamps, "price": prices})

        # Serialize the DataFrame to Arrow format
        table = pa.Table.from_pandas(df)
        sink = pa.BufferOutputStream()
        writer = pa.ipc.new_file(sink, table.schema)
        writer.write_table(table)
        writer.close()
        serialized_data = sink.getvalue().to_pybytes()

        # Return the serialized Arrow data in the response
        return time_series_pb2.TimeSeriesResponse(serialized_series=serialized_data)


async def serve():
    """
    Start the gRPC server.
    """
    server = grpc.aio.server()
    time_series_pb2_grpc.add_TimeSeriesServiceServicer_to_server(
        TimeSeriesService(), server
    )
    server.add_insecure_port("[::]:50051")
    await server.start()
    print("Server started on port 50051.")
    await server.wait_for_termination()


if __name__ == "__main__":
    import asyncio

    asyncio.run(serve())
