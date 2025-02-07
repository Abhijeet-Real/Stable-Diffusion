from transformers import pipeline
import torch
from HuggingFaceLogin import login_to_huggingface
import Config
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def enhance_prompt(prompt: str, model_name: str = "Gustavosta/MagicPrompt-Stable-Diffusion", max_length: int = 50):
    """
    Enhances a short text prompt (1-3 words) into a detailed prompt suitable for image generation using MagicPrompt-Stable-Diffusion.
    
    Parameters:
        prompt (str): The input text (1-3 words) to be expanded into a detailed prompt.
        model_name (str): The Hugging Face model to use for text expansion.
        max_length (int): The maximum length of the expanded prompt (restricted to 50 tokens).
    
    Returns:
        str: The enhanced prompt suitable for image generation.
    """
    # Clear GPU memory before loading model
    torch.cuda.empty_cache()
    
    generator = None  # Initialize generator to avoid UnboundLocalError
    model_source = "Unknown"  # Track where the model was loaded from
    
    try:
        # Attempt to load the model from the local environment (cache)
        generator = pipeline("text-generation", model=model_name,
                              device=0 if torch.cuda.is_available() else -1, 
                              truncation=True,
                              pad_token_id=50256)
        model_source = "Local Environment"
    except Exception:
        logging.warning(f"Failed to load {model_name} from Local Environment, trying Hugging Face Hub")
        
        # Authenticate only when needed
        login_to_huggingface()
        
        try:
            generator = pipeline("text-generation", model=model_name, 
                                 device=0 if torch.cuda.is_available() else -1, 
                                 truncation=True,
                                 pad_token_id=50256)
            model_source = "Hugging Face Hub"
        except Exception as e:
            logging.error(f"Error loading model: {e}")
            return None
    
    if generator is None:
        logging.error(f"Error: {model_name} pipeline could not be initialized.")
        return None
    
    # Generate enhanced prompt with a maximum of 50 tokens
    response = generator(prompt, max_length=max_length, do_sample=True, truncation=True, pad_token_id=50256)
    
    # Clear GPU memory after processing
    torch.cuda.empty_cache()
    
    logging.info(f"{model_name} was loaded from: {model_source}")
    logging.info(f"Enhanced Prompt: {response[0]['generated_text']}")  # Log the enhanced prompt
    
    return response[0]['generated_text']
