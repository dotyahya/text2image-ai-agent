import grpc
from concurrent import futures
import asyncio
import text2image_pb2
import text2image_pb2_grpc
from diffusers import StableDiffusionPipeline
import torch
import io
import signal

from datetime import datetime

class Text2ImageServicer(text2image_pb2_grpc.Text2ImageServicer):
    def __init__(self):
        self.model = StableDiffusionPipeline.from_pretrained(
            "runwayml/stable-diffusion-v1-5",
            safety_checker=None,
            torch_dtype=torch.float32,  # CPU-compatible
            local_files_only=True,      # no online API calls, fetch from ./models
            cache_dir="./models"
        )
        self.model = self.model.to("cpu")
        self.model.enable_attention_slicing()  # CPU memory optimization

    async def GenerateImage(self, request, context):
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{timestamp}] Received request: Text='{request.text}', Context='{request.context}', Style='{request.style}'")

            # input validation
            if not request.text:
                return text2image_pb2.ImageResponse(
                    status="error",
                    message="Text input cannot be empty"
                )

            # combine text, context, and style into a prompt
            prompt = f"{request.text}, {request.context}, {request.style} style"

            # generate image
            image = self.model(prompt, num_inference_steps=5).images[0]  

            # convert image to bytes
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format="PNG")
            img_bytes = img_byte_arr.getvalue()

            print(f"[{timestamp}] Image generation complete.")
            return text2image_pb2.ImageResponse(
                image=img_bytes,
                status="success",
                message=""
            )
            
        except Exception as e:
            return text2image_pb2.ImageResponse(
                status="error",
                message=f"Server error: {str(e)}"
            )

async def serve():
    # create gRPC server with thread pool for concurrency
    server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=10))
    text2image_pb2_grpc.add_Text2ImageServicer_to_server(Text2ImageServicer(), server)
    server.add_insecure_port("[::]:50051")  # listen on port 50051
    
    await server.start()
    print("Server listening on port 50051...")
    
    await server.wait_for_termination()

if __name__ == "__main__":
    asyncio.run(serve())
