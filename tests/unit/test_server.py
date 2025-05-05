import pytest
import grpc
from src import text2image_pb2
from src import text2image_pb2_grpc

def test_generate_image():
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = text2image_pb2_grpc.Text2ImageStub(channel)
        response = stub.GenerateImage(
            text2image_pb2.ImageRequest(
                text="A sunset over a lake",
                context="Travel blog",
                style="realistic"
            )
        )
        assert response.status == "success"
        assert len(response.image) > 0
        assert response.message == ""

def test_empty_text():
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = text2image_pb2_grpc.Text2ImageStub(channel)
        response = stub.GenerateImage(
            text2image_pb2.ImageRequest(
                text="",
                context="Travel blog",
                style="realistic"
            )
        )
        assert response.status == "error"
        assert response.message == "Text input cannot be empty"