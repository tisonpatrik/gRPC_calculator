# grpc/Makefile

PROTO_SRC_DIR := ./proto
PROTO_OUT_DIR := ./src/grpc_api/pb/
PROTOC := python -m grpc_tools.protoc

.PHONY: protos
protos:
	@$(PROTOC) \
		-I/usr/local/include \
		-I$(PROTO_SRC_DIR) \
		--python_out=$(PROTO_OUT_DIR) \
		--grpc_python_out=$(PROTO_OUT_DIR) \
		$(PROTO_SRC_DIR)/time_series.proto
	@echo "Protobuf files compiled successfully!"


.PHONY: clean
clean:
	@rm -f $(PROTO_OUT_DIR)/*_pb2.py
	@rm -f $(PROTO_OUT_DIR)/*_pb2_grpc.py
	@rm -f $(PROTO_OUT_DIR)/*.pyi
	@echo "Cleaned generated Protobuf files."
