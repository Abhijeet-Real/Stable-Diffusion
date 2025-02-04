import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
import random
from Prompt import prompt_list
import Connector

class StableDiffusionApp(toga.App):
    def startup(self):
        # Create the main window
        self.main_window = toga.MainWindow(title="Stable Diffusion Image Generator")  # Set title directly

        # Main layout for the app
        main_box = toga.Box(style=Pack(direction=COLUMN, padding=10))  # Set the initial size here

         # Set the desired window size
        self.main_window.size = (450, 300)

        # Filename input
        filename_label = toga.Label("Filename:", style=Pack(font_weight="bold"))
        self.filename_input = toga.TextInput(placeholder="Enter filename here", style=Pack(width=340))

        filename_box = toga.Box(style=Pack(direction=ROW, padding_bottom=10))
        filename_box.add(filename_label)
        filename_box.add(self.filename_input)

        # Prompt input
        prompt_label = toga.Label("Prompt:", style=Pack(font_weight="bold"))
        self.prompt_input = toga.MultilineTextInput(placeholder="Enter the prompt here...", style=Pack(width=400, height=100))

        prompt_box = toga.Box(style=Pack(direction=COLUMN, padding_bottom=10))
        prompt_box.add(prompt_label)
        prompt_box.add(self.prompt_input)

        # Random Prompt Button
        self.random_button = toga.Button("Random Prompt", on_press=self.set_random_prompt, style=Pack(width=150))
        random_button_box = toga.Box(style=Pack(direction=ROW, padding_bottom=10, alignment="center"))
        random_button_box.add(self.random_button)

        # Inference steps slider
        self.inference_slider = toga.Slider(min=1, max=100, value=40, style=Pack(width=307))
        inference_label = toga.Label("Inference Steps:", style=Pack(font_weight="bold"))
        inference_box = toga.Box(style=Pack(direction=ROW, padding_bottom=10))
        inference_box.add(inference_label)
        inference_box.add(self.inference_slider)

        # Guidance scale slider
        self.guidance_slider = toga.Slider(min=1, max=25, value=15, style=Pack(width=310))
        guidance_label = toga.Label("Guidance Scale:", style=Pack(font_weight="bold"))
        guidance_box = toga.Box(style=Pack(direction=ROW, padding_bottom=2))
        guidance_box.add(guidance_label)
        guidance_box.add(self.guidance_slider)

        # Generate Button
        generate_button = toga.Button("Generate", on_press=self.generate_image, style=Pack(width=150))  # Optional width for consistent centering
        generate_button_box = toga.Box(style=Pack(direction=ROW, padding_top=2, alignment="center"))
        generate_button_box.add(generate_button)


        # Add all components to the main box
        main_box.add(filename_box)
        main_box.add(prompt_box)
        main_box.add(random_button_box)
        main_box.add(inference_box)
        main_box.add(guidance_box)
        main_box.add(generate_button_box)

        self.main_window.content = main_box
        self.main_window.show()

    def set_random_prompt(self, widget):
        # Select a random sublist and use the filename and a random prompt
        random_prompt_data = random.choice(prompt_list)
        filename = random_prompt_data[0]
        random_prompt = random.choice(random_prompt_data[1:])  # Skip filename

        # Set filename and prompt fields
        self.filename_input.value = filename
        self.prompt_input.value = random_prompt

    def generate_image(self, widget):

        Connector.main(object=[str(self.filename_input.value), str(self.prompt_input.value)], \
            num_inference_steps=int(self.inference_slider.value), \
            guidance_scale=int(self.guidance_slider.value),\
            internet = True,\
            fast = True)

        filename = self.filename_input.value
        prompt = self.prompt_input.value
        inference_steps = int(self.inference_slider.value)
        guidance_scale = int(self.guidance_slider.value)

        # Placeholder for actual generation logic
        self.main_window.info_dialog(
            "Image Generated",
            f"Filename: {filename}\nPrompt: {prompt}\nInference Steps: {inference_steps}\nGuidance Scale: {guidance_scale}"
        )

def main():
    return StableDiffusionApp(
        "Stable Diffusion Image Generator",
        "org.None.stablediffusion",
        icon=r"D:\Stable Diffusion\Stable Diffusion Icon.ico"
    )

if __name__ == "__main__":
    main().main_loop()