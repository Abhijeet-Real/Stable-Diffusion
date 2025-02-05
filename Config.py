import os
import warnings
import torch

# Use a relative path based on the working directory
huggingface_cache_dir = os.path.join(os.getcwd(), "HuggingFace", "HuggingFaceCache")

# Create the directory if it does not exist
os.makedirs(huggingface_cache_dir, exist_ok=True)

# Set environment variables for Hugging Face model directory and CUDA settings
os.environ["HF_HOME"] = huggingface_cache_dir
os.environ["CUDA_LAUNCH_BLOCKING"] = "1"
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "max_split_size_mb:128"


def suppress_all_warnings():
    """Suppress all warnings globally."""
    warnings.filterwarnings("ignore")  # Ignore all warnings
    if torch.cuda.is_available():
        torch.backends.cudnn.benchmark = False  # Prevent potential CUDA warnings
    warnings.simplefilter("ignore")


def set_debug_level():
    """Set debug level to warning and handle failures."""
    try:
        os.environ["TRANSFORMERS_VERBOSITY"] = "warning"
        print("Debug level set to WARNING.")
    except Exception as e:
        print(f"Failed to set debug level: {e}")


# Suppress warnings when Config is imported
suppress_all_warnings()
# Set debug level
set_debug_level()
