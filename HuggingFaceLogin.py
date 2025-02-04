from huggingface_hub import login
import Config

# Ensure user is logged in
def login_to_huggingface(file_path=r"D:\Stable Diffusion\Hugging Face"):
    token, username, website = None, None, None
    try:
        with open(file_path, "r") as file:
            lines = file.readlines()
            for line in lines:
                if line.startswith("Token:"):
                    token = line.split("Token:")[1].strip()
                elif line.startswith("User_Name:"):
                    username = line.split("User_Name:")[1].strip()
                elif line.startswith("Website:"):
                    website = line.split("Website:")[1].strip()
        
        if token:
            login(token)
            print(f"Logged in as {username} on {website}")
        else:
            print("Token not found. Please check the file.")
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except Exception as e:
        print(f"Login failed:")
        