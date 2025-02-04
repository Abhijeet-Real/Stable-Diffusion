from diffusers import StableDiffusion3Pipeline
import torch
from HuggingFaceLogin import login_to_huggingface
import Config

# Function to generate an image using Stable Diffusion 3.5 with customizable parameters
def generate_image(prompt, num_inference_steps=30, guidance_scale=5, internet=True, fast=True): 

    # Clear cache before generating the image
    torch.cuda.empty_cache()

    pipe = None  # Initialize pipe to avoid UnboundLocalError

    # Define the model
    medium_35 = "stabilityai/stable-diffusion-3.5-medium"
    
    try:
        # Attempt to load the model with Local environment
        pipe = StableDiffusion3Pipeline.from_pretrained(
            medium_35, torch_dtype=torch.float16, local_files_only=True
        ).to("cuda")
        
    except Exception as e: 
        print(f"Failed to load {medium_35} from Local environment") 

        if not internet:
            return None
        
        # Attempt login
        login_to_huggingface()
        
        # Try loading the model from Hugging Face hub
        try:
            pipe = StableDiffusion3Pipeline.from_pretrained(
                medium_35, torch_dtype=torch.float16, local_files_only=False
            ).to("cuda")
        except Exception as e_local:
            print(e_local, "Couldn't connect to the Hub.")
            return None  # Exit if model cannot be loaded
        else:
            print(f"Loaded {medium_35} from Hub.")
    else:
        print(f"Loaded {medium_35} from Local environment")
    
    if pipe is None:
        print(f"Error: {medium_35} pipeline could not be initialized.")
        return None

    if fast:
        # Enable memory-saving options
        pipe.enable_attention_slicing()
        pipe.enable_model_cpu_offload()
        pipe.enable_sequential_cpu_offload()

    torch.cuda.empty_cache()
    torch.cuda.reset_max_memory_allocated()

    # Generate the image with specified enhanced_prompt and parameters
    image = pipe(prompt, num_inference_steps=num_inference_steps, guidance_scale=guidance_scale).images[0]

    return image