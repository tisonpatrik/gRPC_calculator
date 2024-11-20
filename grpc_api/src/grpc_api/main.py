import asyncio
import logging
from datetime import datetime, timedelta

import grpc
import numpy as np
import pandas as pd
import pyarrow as pa

from grpc_api.pb import time_series_pb2, time_series_pb2_grpc

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create a console handler and set the log format
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
console_handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(console_handler)

class TimeSeriesService(time_series_pb2_grpc.TimeSeriesServiceServicer):
    async def GenerateTimeSeries(self, request, context):
        """
        Generate a time series of the specified length using Apache Arrow for serialization.
        """
        try:
            length = request.length
            if length <= 0:
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details("Length must be a positive integer.")
                return time_series_pb2.TimeSeriesResponse()

            start_time = datetime.now()

            # Generate timestamps and random prices
            timestamps = [start_time + timedelta(minutes=i) for i in range(length)]
            prices = np.random.uniform(10, 100, size=length)

            # Create a Pandas DataFrame
            df = pd.DataFrame({"time": timestamps, "price": prices})
            logger.info(f"Generated time series with {length} rows")

            # Serialize the DataFrame to Arrow format
            table = pa.Table.from_pandas(df)
            sink = pa.BufferOutputStream()
            writer = pa.ipc.new_file(sink, table.schema)
            writer.write_table(table)
            writer.close()
            serialized_data = sink.getvalue().to_pybytes()

            # Return the serialized Arrow data in the response
            logger.info("Serialized time series data successfully.")
            return time_series_pb2.TimeSeriesResponse(serialized_series=serialized_data)

        except Exception as e:
            logger.exception("Error generating time series")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("An error occurred while generating the time series.")
            return time_series_pb2.TimeSeriesResponse()

async def serve():
    """
    Start the gRPC server.
    """
    server = grpc.aio.server()
    time_series_pb2_grpc.add_TimeSeriesServiceServicer_to_server(
        TimeSeriesService(), server
    )
    server.add_insecure_port("[::]:50051")

    try:
        logger.info("Starting gRPC server on port 50051")
        await server.start()
        logger.info("Server started. Waiting for requests...")
        await server.wait_for_termination()
    except Exception as e:
        logger.exception("Error starting server")
    finally:
        logger.info("Stopping gRPC server")
        await server.stop(0)

if __name__ == "__main__":
    asyncio.run(serve())
