# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: fake.proto
# Protobuf Python Version: 5.28.1
"""Generated protocol buffer code."""

from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder

_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC, 5, 28, 1, "", "fake.proto"
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\nfake.proto\x12\x04\x66\x61ke"G\n\x15\x46\x61keTimeSeriesRequest\x12\x0e\n\x06length\x18\x01 \x01(\x05\x12\x0e\n\x06source\x18\x02 \x01(\t\x12\x0e\n\x06\x66ilter\x18\x03 \x01(\t"E\n\x16\x46\x61keTimeSeriesResponse\x12\x19\n\x11serialized_series\x18\x01 \x01(\x0c\x12\x10\n\x08metadata\x18\x02 \x01(\t2\x97\x02\n\x15\x46\x61keTimeSeriesService\x12S\n\x16GenerateFakeTimeSeries\x12\x1b.fake.FakeTimeSeriesRequest\x1a\x1c.fake.FakeTimeSeriesResponse\x12V\n\x19GetFakeTimeSeriesMetadata\x12\x1b.fake.FakeTimeSeriesRequest\x1a\x1c.fake.FakeTimeSeriesResponse\x12Q\n\x14\x44\x65leteFakeTimeSeries\x12\x1b.fake.FakeTimeSeriesRequest\x1a\x1c.fake.FakeTimeSeriesResponseb\x06proto3'  # noqa: E501
)

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, "fake_pb2", _globals)
if not _descriptor._USE_C_DESCRIPTORS:
    DESCRIPTOR._loaded_options = None
    _globals["_FAKETIMESERIESREQUEST"]._serialized_start = 20
    _globals["_FAKETIMESERIESREQUEST"]._serialized_end = 91
    _globals["_FAKETIMESERIESRESPONSE"]._serialized_start = 93
    _globals["_FAKETIMESERIESRESPONSE"]._serialized_end = 162
    _globals["_FAKETIMESERIESSERVICE"]._serialized_start = 165
    _globals["_FAKETIMESERIESSERVICE"]._serialized_end = 444
# @@protoc_insertion_point(module_scope)