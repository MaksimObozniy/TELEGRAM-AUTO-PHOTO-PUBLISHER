import requests
import os
import argparse
from utils_function.create_folder import create_folder
from utils_function.saving_photos import saving_photos


def download_spacex_launch_photos(launch_id, folder_name="Spacex_images"):
    
    create_folder(folder_name)
    
    url = f"https://api.spacexdata.com/v5/launches/{launch_id}"
    
    response = requests.get(url)
    response.raise_for_status()
    
    launch_data = response.json()
    
    links = launch_data.get("links")
    
    image_urls = []
    if links:
        flickr = links.get("flickr")
        if flickr:
            image_urls = flickr.get("original", [])
       
       
    if not image_urls:
        print("Нет изображений для скачивания")
        return
    
    for index, photo in enumerate(image_urls, start=1):
        file_name = f"spacex{index}.jpg"
        file_path = os.path.join(folder_name, file_name)
        
        saving_photos(photo, file_path, params=None)


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="Скрипт для скачивания фотографий запусков SpaceX ")
    parser.add_argument("-launch_id", type=str, default="5eb87d46ffd86e000604b388", help="ID запуска ракет. По умолчанию стоит запуск 'latest'")
    args = parser.parse_args()
    
    download_spacex_launch_photos(args.launch_id)