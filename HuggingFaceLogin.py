from huggingface_hub import login
import Config
import os
import logging

# Ensure user is logged in
def login_to_huggingface(file_path="Hugging Face"):  # Relative Path
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
            logging.info(f"Logged in as {username} on {website}")
        else:
            logging.error("Token not found. Please check the file.")
    except FileNotFoundError:
        logging.error(f"Error: The file '{file_path}' was not found.")
    except Exception as e:
        logging.error("Login failed:", str(e))
