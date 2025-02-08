import logging

import torch
from diffusers import StableDiffusion3Pipeline
from transformers import CLIPTokenizer

from HuggingFaceLogin import login_to_huggingface
import Config


# Function to generate an image using Stable Diffusion 3.5 with customizable parameters
def generate_image(prompt, num_inference_steps=40, guidance_scale=25): 

    # Clear cache before generating the image
    torch.cuda.empty_cache()

    pipe = None  # Initialize pipe to avoid UnboundLocalError

    # Define the model
    model = "stabilityai/stable-diffusion-3.5-medium"

    tokenizer = CLIPTokenizer.from_pretrained("openai/clip-vit-large-patch14")
    
    try:
        # Attempt to load the model with Local environment
        pipe = StableDiffusion3Pipeline.from_pretrained(
            model, torch_dtype=torch.float16, local_files_only=True, tokenizer=tokenizer
        ).to("cuda")
        logging.info(f"Loaded {model} from Local environment")

    except Exception as e: 
        logging.error(f"Failed to load {model} from Local environment: {e}")        
        # Attempt login
        login_to_huggingface()
        
        # Try loading the model from Hugging Face hub
        try:
            pipe = StableDiffusion3Pipeline.from_pretrained(
                model, torch_dtype=torch.float16, local_files_only=False, tokenizer=tokenizer
            ).to("cuda")
            logging.info(f"Loaded {model} from Hugging Face Hub")
        except Exception as e_local:
            logging.error(f"Error loading model from Hugging Face Hub: {e_local}")
            return None  # Exit if model cannot be loaded
    
    if pipe is None:
        logging.error(f"Error: {model} pipeline could not be initialized.")
        return None

    # Enable memory-saving options
    pipe.enable_attention_slicing()
    pipe.enable_model_cpu_offload()
    pipe.enable_sequential_cpu_offload()

    torch.cuda.empty_cache()
    torch.cuda.reset_max_memory_allocated()

    # Generate the image with specified enhanced_prompt and parameters
    image = pipe(prompt, num_inference_steps=num_inference_steps, guidance_scale=guidance_scale).images[0]
    
    return image