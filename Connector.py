import os
import Prompt
import random
from MagicPrompt import enhance_prompt
import Config

def generate_unique_filename(filename):
    """
    Generates a unique filename by appending a number if the file already exists.
    
    Parameters:
        filename (str): The initial filename to check for uniqueness.
    
    Returns:
        str: A unique filename with a numerical suffix if necessary, ensuring a .png extension.
    """
    base, ext = os.path.splitext(filename)  # Split filename into name and extension
    if not ext:
        ext = ".png"  # Add .png if there’s no extension
    elif ext.lower() != ".png":
        base = f"{base}{ext}"
        ext = ".png"  # Ensure the extension is .png

    filename = f"{base}{ext}"
    counter = 1
    
    # Loop to check if file exists and append a number if necessary
    while os.path.exists(os.path.join("Images", filename)):
        filename = f"{base} {counter}{ext}"
        counter += 1

    return filename

def main(object = None, num_inference_steps = 1, guidance_scale = 1, internet = True, fast = True):

    # Picks a prompt for me from predefined prompt
    if object is None:
        object = random.choice(Prompt.prompt_list)
        prompt = random.choice(object[1:])
    else:
        filename = object[0]
        prompt = object[1]
        prompt = enhance_prompt(prompt)

    # Now import the module and call generate_image
    from StableDiffusion35 import generate_image
    image = generate_image(prompt=prompt, num_inference_steps=num_inference_steps, guidance_scale=guidance_scale)

    # Save the generated image to the specified filename
    filename = generate_unique_filename(object[0])
    # Ensure the "Images" folder exists
    os.makedirs("Images", exist_ok=True)
    image.save(os.path.join("Images", filename))
    print(f"Image saved as {filename}")