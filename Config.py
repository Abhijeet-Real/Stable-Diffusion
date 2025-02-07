import os
import warnings
import logging

# Use a relative path based on the working directory
huggingface_cache_dir = os.path.join(os.getcwd(), "HuggingFace", "HuggingFaceCache")

# Create the directory if it does not exist
os.makedirs(huggingface_cache_dir, exist_ok=True)

# Set environment variables for Hugging Face model directory and CUDA settings
os.environ["HF_HOME"] = huggingface_cache_dir
os.environ["CUDA_LAUNCH_BLOCKING"] = "1"
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

# Configure logging
logging.basicConfig(level=logging.WARNING, format='%(asctime)s - %(levelname)s - %(message)s')

warnings.filterwarnings("ignore")  # Ignore all warnings