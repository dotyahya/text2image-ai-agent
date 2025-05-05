import os
import grpc
import re
import text2image_pb2
import text2image_pb2_grpc

OUTPUT_DIR = "outputs"

# helper to store images as IMG### (e.g., IMG001, IMG002 and so on...)
def get_next_image_filename():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    existing_files = os.listdir(OUTPUT_DIR)
    image_numbers = [
        int(re.findall(r"IMG(\d{3})\.png", f)[0])
        for f in existing_files if re.match(r"IMG\d{3}\.png", f)
    ]
    next_number = max(image_numbers, default=0) + 1
    return os.path.join(OUTPUT_DIR, f"IMG{next_number:03}.png")

def generate_image(text, context, style):
    # connect to the gRPC server listening on port 50051
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = text2image_pb2_grpc.Text2ImageStub(channel)

        # send request
        response = stub.GenerateImage(
            text2image_pb2.ImageRequest(
                text=text,
                context=context,
                style=style
            )
        )

        # process response
        if response.status == "success":
            output_path = get_next_image_filename()
            with open(output_path, "wb") as f:
                f.write(response.image)
            return f"Image saved as {output_path}"
        else:
            return f"Error: {response.message}"

if __name__ == "__main__":
    result = generate_image(
        text="A futuristic cityscape",
        context="at night with neon lights",
        style="cyberpunk"
    )
    print(result)