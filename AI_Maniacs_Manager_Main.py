from AI_Picture_Creater.ImageGenerator import ImageGenerator
import FileReader
from Video_Creater.VideoCreater import VideoCreator
import pandas as pd
from YouTube_Uploader.VideoUploader import VideoUploader, YouTubeService, Video

def create_images(project_folder_path):
    api_key = FileReader.read_api_key()
    image_generator = ImageGenerator(api_key, project_folder_path)
    image_generator.generate_and_save_images(excel_path=project_folder_path + "\\prompts.xlsx", image_size="1024x1024", image_amount=1)

def create_video(project_folder_path):
    picture_path = project_folder_path + "\\Pictures"
    captions_path =  project_folder_path + "\\captions.xlsx"
    background_music = FileReader.find_mp3_file(project_folder_path)

    # Загрузка подписей из Excel-файла
    captions_list = pd.read_excel(captions_path, engine='openpyxl').iloc[:, 0].tolist()


    video_creator = VideoCreator(picture_path, captions_list, background_music, project_folder_path)
    video_creator.create_video()

def upload_video(project_folder_path):
    scopes = ["https://www.googleapis.com/auth/youtube.upload"]
    video_category_id =  "24"
    video_path = project_folder_path + "\\final_video.mp4"

    print("\nPlease enter the following details for your video:")
    insertedValues = {}
    fields = ["Title", "Description", "Privacy Status"]
    valid_privacy_statuses = ["public", "private", "unlisted"]

    for field in fields:
        while True:
            value = input(f"{field}: ")

            # Для "Privacy Status" проверяем, соответствует ли значение одному из допустимых статусов
            if field == "Privacy Status" and value.lower() not in valid_privacy_statuses:
                print("Error: Privacy Status must be 'public', 'private', or 'unlisted'.")
                continue  # Продолжаем цикл для повторного ввода

            # Проверка на пустое значение для специфических полей
            if field == "Privacy Status" and not value.strip():
                print(f"{field} cannot be empty. Please enter a valid value.")
                continue  # Продолжаем цикл для повторного ввода

            insertedValues[field] = value
            break

    youtube_service = YouTubeService("client_secret.json", scopes).get_service()
    video_data = Video(categoryId=video_category_id, title=insertedValues['Title'], 
                            description=insertedValues['Description'],
                            privacyStatus=insertedValues['Privacy Status'], path=video_path)
            
    uploader = VideoUploader(youtube_service, video_data)
    response = uploader.upload_video()
    print(response)


def main():
    
    input("Press Enter to start...")

    project_folder_path = input("\nPEnter the \033[1mfull path to the project folder\033[0m 📁: ").replace('"', '').strip()

    create_images(project_folder_path)

    input("\nPictures created successfully!✅\nPlease check the result and press Enter when you are ready.\nRemember❗️you need to \033[1madd background music and captions.\033[0m\n")

    create_video(project_folder_path)

    input("\nVideo created successfully!✅\nPlease check the result and press Enter when you are ready.")

    upload_video(project_folder_path)


if __name__ == "__main__":
    main()