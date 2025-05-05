FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# generate gRPC stubs
RUN python -m grpc_tools.protoc -I. --python_out=src --grpc_python_out=src src/text2image.proto

# run server to listen on port 50051
CMD ["python", "src/server.py"]