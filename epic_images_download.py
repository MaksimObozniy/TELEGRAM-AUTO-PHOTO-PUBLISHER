import os
import requests
from utils_function.create_folder import create_folder
from utils_function.saving_photos import saving_photos
from datetime import datetime




def download_nasaepic_photo(api_key, folder_name="EPIC_images"):
    
    api_url = "https://api.nasa.gov/EPIC/api/natural/images"
    params = {"api_key": api_key}
    
    response = requests.get(api_url, params=params)
    response.raise_for_status()
    epic_data = response.json()
    
    create_folder(folder_name)
    
    for index, photo_data in enumerate(epic_data, start=1):
        
        date_object = datetime.fromisoformat(photo_data['date'].split(" ")[0])
        
        year = date_object.strftime("%Y")
        month = date_object.strftime("%m")
        day = date_object.strftime("%d")
        
        image_name = photo_data['image']
        
        image_url = f"https://api.nasa.gov/EPIC/archive/natural/{year}/{month}/{day}/png/{image_name}.png"
        
        file_name = f"epic_{index}.png"
        file_path = os.path.join(folder_name, file_name)
        
        saving_photos(image_url, file_path, params)
            
            
if __name__ == "__main__":
    
    NASA_API_KEY = os.getenv("NASA_API_KEY")
    download_nasaepic_photo(NASA_API_KEY)
