import requests

def saving_photos(image_url, file_path, params=None):
    
    img_response = requests.get(image_url, params=params)
    img_response.raise_for_status()
        
    with open(file_path, 'wb') as file:
        file.write(img_response.content)