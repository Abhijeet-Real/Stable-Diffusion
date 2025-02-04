import os
import warnings
import torch

AA02_dir_path = r"D:\Stable Diffusion\HuggingFace\HuggingFaceCache"
# Create the directory if it does not exist
os.makedirs(AA02_dir_path, exist_ok=True)
# Set environment variables for Hugging Face model directory and CUDA settings

os.environ["HF_HOME"] = AA02_dir_path
os.environ["CUDA_LAUNCH_BLOCKING"] = "1"
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "max_split_size_mb:128"


def suppress_all_warnings():
    """Suppress all warnings globally."""
    warnings.filterwarnings("ignore")  # Ignore all warnings
    if torch.cuda.is_available():
        torch.backends.cudnn.benchmark = False  # Prevent potential CUDA warnings
    warnings.simplefilter("ignore")


# Suppress warnings when Config is imported
suppress_all_warnings()
