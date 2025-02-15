# Stable Diffusion GUI

## Overview
Stable Diffusion GUI is a PyQt5-based application for generating AI-generated images using Stable Diffusion. The interface allows users to input prompts, configure inference settings, and generate images seamlessly. The project integrates **Hugging Face** for model access and caching, ensuring an optimized user experience.

## Features
- **Graphical User Interface (GUI)** for Stable Diffusion.
- **Prompt randomization** for creative image generation.
- **Adjustable inference steps and guidance scale**.
- **Multithreading support** to prevent UI freezing during image generation.
- **Hugging Face integration** for authentication and model management.
- **Configurable environment settings** for GPU optimization.

## Installation
### Prerequisites
Ensure you have the following installed:
- Python 3.8+
- PyQt5
- Pillow
- Hugging Face Hub
- Torch and CUDA (for GPU acceleration)

### Setup
1. Clone the repository:
   ```sh
   git clone https://github.com/Abhijeet-Real/stable-diffusion.git
   cd stable-diffusion-gui
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Configure Hugging Face login credentials (see below).
4. Run the application:
   ```sh
   python StableDiffusionGUI.py
   ```

## Hugging Face Authentication
To use Hugging Face models, authentication is required. Create a file named `Hugging Face` inside the project directory with the following format:

```
Website: https://huggingface.co
User_Name: Your Hugging Face User Name
Token_Name: Your Hugging Face Token Name
Token: Your Hugging Face Token
```

### Logging into Hugging Face
The application reads the credentials from the `Hugging Face` file and logs in automatically.

## Configuration
This project uses relative paths for environment settings and resource files.
- **Cache Directory:** The Hugging Face model cache is stored inside `HuggingFace/HuggingFaceCache`.
- **Environment Variables:**
  - `HF_HOME` → Sets the Hugging Face model cache location.
  - `CUDA_LAUNCH_BLOCKING=1` → Enables CUDA debugging.
  - `HF_HUB_DISABLE_SYMLINKS_WARNING=1` → Suppresses Hugging Face warnings.
  - `PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:128` → Optimizes GPU memory allocation.
- **GUI Assets:**
  - `Stable Diffusion Icon.ico` → Application icon.
  - `Stable Diffusion Background.jpg` → Background image.

## Usage
1. **Launch the GUI**.
2. **Enter a filename and prompt** or use **Random Prompt**.
3. **Adjust inference steps and guidance scale** as needed.
4. **Click Generate** to create an AI-generated image.
5. Once completed, the image is saved and a success message is displayed.

## Known Issues & Troubleshooting
- Ensure the Hugging Face credentials file exists and is correctly formatted.
- If models fail to load, check GPU compatibility and **install CUDA** if needed.
- Run the application from the `D:\Stable Diffusion` directory to avoid relative path issues.

## Contributing
Feel free to fork and contribute via pull requests!

## License
This project is open-source and available under the MIT License.
