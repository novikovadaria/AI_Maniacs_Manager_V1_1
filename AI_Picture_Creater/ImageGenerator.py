import requests
import openai
import os
import pandas as pd
from datetime import datetime

class ImageGenerator:
    def __init__(self, api_key, storage_path):
        self.api_key = api_key
        self.storage_path = storage_path

    def generate_and_save_images(self, excel_path, image_size, image_amount):
        openai.api_key = self.api_key
        list_of_prompts = pd.read_excel(excel_path, engine='openpyxl').iloc[:, 0].tolist()

        # Создаем путь к директории
        directory_path = os.path.join(self.storage_path, "Pictures")
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)

        for index, prompt in enumerate(list_of_prompts, start=1):
            print(f"\nProcessing prompt {index} of {len(list_of_prompts)} 🔄: '{prompt}'")
            image_url = self.create_image(prompt, image_size, image_amount)
            self.save_image_to_file(image_url, prompt, directory_path)

    def create_image(self, prompt, image_size, image_amount):
        print(f"Creating image 🎨🖌: '{prompt}'...")
        response = openai.Image.create(
            prompt=prompt,
            n=image_amount,
            size=image_size
        )
        image_url = response['data'][0]['url']
        print("Image is created successfully.✅")
        return image_url

    def save_image_to_file(self, image_url, prompt, directory_path):
        print(f"Saving image 💾: '{prompt}'...")
        valid_prompt = "".join(char for char in prompt if char.isalnum() or char in (" ", "-", "_")).rstrip()
        prompt_directory_path = os.path.join(directory_path, valid_prompt)
        if not os.path.exists(prompt_directory_path):
            os.makedirs(prompt_directory_path)

        file_path = os.path.join(prompt_directory_path, f"{valid_prompt}.jpg")

        response = requests.get(image_url)
        if response.status_code == 200:
            with open(file_path, "wb") as file:
                file.write(response.content)
            print("Image is saved successfully.✅")
        else:
            print("Error: could not save the image.❌")

