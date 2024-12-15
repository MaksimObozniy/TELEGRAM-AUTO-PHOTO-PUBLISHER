import requests
import os
import argparse
from utils_function.create_folder import create_folder
from utils_function.saving_photos import saving_photos


def fetch_spacex_launch(launch_id):
    
    folder_name = "Spacex_images"
    create_folder(folder_name)
    
    url = f"https://api.spacexdata.com/v5/launches/{launch_id}"
    
    response = requests.get(url)
    response.raise_for_status()
    
    launch_data = response.json()
    
    links = launch_data.get("links")
    
    images_url = []
    if links:
        flickr = links.get("flickr")
        if flickr:
            images_url = flickr.get("original", [])
       
       
    if not images_url:
        print("Нет изображений для скачивания")
        return
    
    for index, image_url in enumerate(images_url, start=1):
        file_name = f"spacex{index}.jpg"
        file_path = os.path.join(folder_name, file_name)
        
        saving_photos(image_url, file_path, params="")


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="Скрипт для скачивания фотографий запусков SpaceX ")
    parser.add_argument("-launch_id", type=str, default="5eb87d46ffd86e000604b388", help="ID запуска ракет. По умолчанию стоит запуск 'latest'")
    args = parser.parse_args()
    
    fetch_spacex_launch(args.launch_id)