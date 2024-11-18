# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""

import grpc

from grpc_api.pb import time_series_pb2 as time__series__pb2

GRPC_GENERATED_VERSION = "1.68.0"
GRPC_VERSION = grpc.__version__
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower

    _version_not_supported = first_version_is_lower(
        GRPC_VERSION, GRPC_GENERATED_VERSION
    )
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    raise RuntimeError(
        f"The grpc package installed is at version {GRPC_VERSION},"
        + " but the generated code in time_series_pb2_grpc.py depends on"
        + f" grpcio>={GRPC_GENERATED_VERSION}."
        + f" Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}"
        + f" or downgrade your generated code using grpcio-tools<={GRPC_VERSION}."
    )


class TimeSeriesServiceStub(object):
    """Service definition for generating time series data"""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GenerateTimeSeries = channel.unary_unary(
            "/time_series.TimeSeriesService/GenerateTimeSeries",
            request_serializer=time__series__pb2.TimeSeriesRequest.SerializeToString,
            response_deserializer=time__series__pb2.TimeSeriesResponse.FromString,
            _registered_method=True,
        )


class TimeSeriesServiceServicer(object):
    """Service definition for generating time series data"""

    def GenerateTimeSeries(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")


def add_TimeSeriesServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
        "GenerateTimeSeries": grpc.unary_unary_rpc_method_handler(
            servicer.GenerateTimeSeries,
            request_deserializer=time__series__pb2.TimeSeriesRequest.FromString,
            response_serializer=time__series__pb2.TimeSeriesResponse.SerializeToString,
        ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
        "time_series.TimeSeriesService", rpc_method_handlers
    )
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers(
        "time_series.TimeSeriesService", rpc_method_handlers
    )


# This class is part of an EXPERIMENTAL API.
class TimeSeriesService(object):
    """Service definition for generating time series data"""

    @staticmethod
    def GenerateTimeSeries(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/time_series.TimeSeriesService/GenerateTimeSeries",
            time__series__pb2.TimeSeriesRequest.SerializeToString,
            time__series__pb2.TimeSeriesResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True,
        )
