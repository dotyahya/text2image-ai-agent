from diffusers import StableDiffusionPipeline
import torch

def download_model():
    model_id = "runwayml/stable-diffusion-v1-5"
    pipe = StableDiffusionPipeline.from_pretrained(
        model_id,
        torch_dtype=torch.float32,  # float32 for CPU inference
        cache_dir="./models"  # store weights locally
    )
    print("Model downloaded successfully!")

if __name__ == "__main__":
    download_model()