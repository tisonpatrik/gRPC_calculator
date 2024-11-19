# grpc/Makefile

PROTO_SRC_DIR := ./proto
PROTO_OUT_DIR := ./src/grpc_api/pb/
PROTOC := python -m grpc_tools.protoc
PROTOC_GEN_MYPY := python -m mypy_protobuf.main

# Find all .proto files in the source directory
PROTO_FILES := $(wildcard $(PROTO_SRC_DIR)/*.proto)

.PHONY: protos
protos:
	@for proto_file in $(PROTO_FILES); do \
		$(PROTOC) \
			-I/usr/local/include \
			-I$(PROTO_SRC_DIR) \
			--python_out=$(PROTO_OUT_DIR) \
			--grpc_python_out=$(PROTO_OUT_DIR) \
			--mypy_out=$(PROTO_OUT_DIR) \
			$$proto_file; \
	done
	@echo "Protobuf files compiled successfully with mypy stubs!"
