import tkinter as tk
from tkinter import messagebox
from Connector import main
import CustomIcon as CI
import random
import Prompt

# Define the function to handle the generation process
def generate_image():
    filename = filename_entry.get()
    prompt = prompt_entry.get("1.0", tk.END).strip()
    num_inference_steps = steps_slider.get()
    guidance_scale = scale_slider.get()
    
    # Define prompt object format for main function
    object = [filename, prompt]

    internet = True if internet_button.cget('relief') == 'sunken' else False
    fast = True if fast_button.cget('relief') == 'sunken' else False
    
    # Call the main function from ImageGenAI with inputs
    main(object=object, num_inference_steps=num_inference_steps, guidance_scale=guidance_scale, internet = internet, fast = fast)
    messagebox.showinfo("Success", f"Image generated and saved as {filename}.")

# Function to pick a new random prompt and update the prompt box
def update_prompt_filename():
    object = random.choice(Prompt.prompt_list)
    new_prompt = random.choice(object[1:]).strip()
    
    filename_entry.delete(0, tk.END)
    filename_entry.insert(0, object[0])
    prompt_entry.delete("1.0", tk.END)
    prompt_entry.insert("1.0", new_prompt)

# Toggle functions for Internet and Fast Mode
def toggle_internet():
    if internet_button.cget('relief') == 'sunken':
        internet_button.config(bg='SystemButtonFace', relief='raised', text="Internet Off")
    else:
        internet_button.config(bg='green', relief='sunken', text="Internet On")

def toggle_fast_mode():
    if fast_button.cget('relief') == 'sunken':
        fast_button.config(bg='SystemButtonFace', relief='raised', text="Fast Disabled")
    else:
        fast_button.config(bg='green', relief='sunken', text="Fast Enabled")

# Set up the GUI window
root = tk.Tk()
root.title("Stable Diffusion Image Generator")
icon_address = "D:\Stable Diffusion\Stable Diffusion Icon.ico"
CI.set(root, icon_address)

# Filename input (adjust width to match prompt box width)
tk.Label(root, text="Filename:").grid(row=0, column=0, padx=10, pady=5)
filename_entry = tk.Entry(root, width=53, )  # Set width to match prompt box
filename_entry.grid(row=0, column=1, padx=10, pady=5, columnspan=2)  # Span two columns to align

# Prompt input (multi-line for paragraph)
tk.Label(root, text="Prompt:").grid(row=1, column=0, padx=10, pady=5)
prompt_entry = tk.Text(root, height=8, width=40, wrap="word")
prompt_entry.grid(row=1, column=1, padx=10, pady=5, columnspan=2)

# Insert initial prompt and filename
update_prompt_filename()

# New Random Prompt button
new_prompt_button = tk.Button(root, text="New Random Prompt", width = 45, command=update_prompt_filename)
new_prompt_button.grid(row=2, column=1, padx=5, pady=5, columnspan=2)

# Slider for Number of Inference Steps
tk.Label(root, text="Inference Steps:").grid(row=3, column=0, padx=10, pady=5)
steps_slider = tk.Scale(root, from_=1, to=100, length = 325, orient="horizontal")
steps_slider.set(40)  # Default value
steps_slider.grid(row=3, column=1, padx=10, pady=5, columnspan=2)

# Slider for Guidance Scale
tk.Label(root, text="Guidance Scale:").grid(row=4, column=0, padx=10, pady=5)
scale_slider = tk.Scale(root, from_=1, to=25, length = 325, orient="horizontal")
scale_slider.set(15)  # Default value
scale_slider.grid(row=4, column=1, padx=10, pady=5, columnspan=2)

internet_button = tk.Button(root, text="Internet Off", bg='SystemButtonFace', relief='raised',width=20, command=toggle_internet)
internet_button.grid(row=5, column=1, padx=5, pady=5, sticky="w")

fast_button = tk.Button(root, text="Fast Disabled", bg='SystemButtonFace', relief='raised', width=20, command=toggle_fast_mode)
fast_button.grid(row=5, column=2, padx=5, pady=5, sticky="e")

# Generate button
generate_button = tk.Button(root, text="Generate", command=generate_image, width = 47)
generate_button.grid(row=6, column=1, columnspan=2, pady=10)

# Run the Tkinter event loop
root.mainloop()
