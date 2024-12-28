import telegram
import argparse
import os
import random
import time
from dotenv import load_dotenv


def get_photo_list(photos_directory):
    
    photos =[]
    for root, _, files in os.walk(photos_directory):
        for file in files:
            if file.lower().endswith((".jpg", ".jpeg", ".png")):
                photos.append(os.path.join(root, file))
    return photos

def scan_file_size(photo_path, max_file_size_mb=20):
    file_size = os.path.getsize(photo_path) / (1024 * 1024)
    
    if file_size > max_file_size_mb:
        return False
    return True
    
    
def publish_photo(photo_path, bot, telegram_chat_id):
    with open(photo_path, 'rb') as photo:
        bot.send_photo(chat_id=telegram_chat_id, photo=photo)
        print(f"Фото опубликовано {photo_path}")


def execution_main_logic(time_delay, bot, telegram_chat_id, photos_directory, max_file_size_mb):
    photos = get_photo_list(photos_directory)
    random.shuffle(photos)
    
    while True:
        for photo_path in photos:
            if scan_file_size(photo_path, max_file_size_mb):
                publish_photo(photo_path, bot, telegram_chat_id)
                time.sleep(time_delay)
            else:
                print(f"Пропущено из-за размера: {photo_path}")
        random.shuffle(photos)


def main():
    load_dotenv()
    
    telegram_bot_token = os.environ['TELEGRAM_BOT_TOKEN']
    telegram_chat_id = os.environ['TELEGRAM_CHAT_ID']
    photos_directory = os.getenv('PHOTOS_DIRECTORY', default=os.getcwd())
    
    
    bot = telegram.Bot(token=telegram_bot_token)
    
    parser = argparse.ArgumentParser(description="Запуск бота для отправки фото в мессенджер Телеграм")
    parser.add_argument("-time_delay", 
                        type=int, 
                        default=14400, 
                        help="Задержка времени перед отправкой фотографии (стандартное значение 4 часа: 14400 секунд)")
    args = parser.parse_args()
    
    execution_main_logic(args.time_delay, bot, telegram_chat_id, photos_directory, max_file_size_mb=20)
    
    
if __name__ == "__main__":
    main()    