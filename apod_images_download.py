from utils_function.create_folder import create_folder
from utils_function.saving_photos import saving_photos
import requests
import os


def download_nasa_apod_photos(api_key, folder_name="Apod_images"):
    
    url_api = "https://api.nasa.gov/planetary/apod"
    
    params = {
        "api_key": api_key,
        "count": 30
    }
    
    response = requests.get(url_api, params=params)
    response.raise_for_status()
    
    create_folder(folder_name)
    
    data_photo_day = response.json()
    
    for index, photo_data in enumerate(data_photo_day, start=1):
        image_url = photo_data.get("hdurl")
        
        if not image_url:
            continue
        
        file_name = f"apod_{index}.jpg"
        file_path = os.path.join(folder_name, file_name)
        
        saving_photos(image_url, file_path, params='')
            

if __name__ == "__main__":
    NASA_API_KEY = os.environ['NASA_API_KEY']
    
    download_nasa_apod_photos(NASA_API_KEY)
    