from diffusers import StableDiffusionPipeline
import torch

class Text2ImageServicer(text2image_pb2_grpc.Text2ImageServicer):
    def __init__(self):
        self.model = StableDiffusionPipeline.from_pretrained(
            "runwayml/stable-diffusion-v1-5",
            torch_dtype=torch.float32,
            local_files_only=True,
            cache_dir="./models"
        )
        self.model = self.model.to("cpu")
        self.model.enable_attention_slicing()  # CPU optimization