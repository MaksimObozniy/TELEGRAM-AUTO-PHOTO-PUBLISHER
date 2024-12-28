import telegram
import argparse
import os
import random
import time
from dotenv import load_dotenv


def get_photo_list(pars_directory):
    
    photos =[]
    for root, _, files in os.walk(pars_directory):
        for file in files:
            if file.lower().endswith((".jpg", ".jpeg", ".png")):
                photos.append(os.path.join(root, file))
    return photos

def scan_file_size(photo_path, max_file_size_mb):
    file_size = os.path.getsize(photo_path) / (1024 * 1024)
    
    if file_size > max_file_size_mb:
        return False
    return True
    
    
def publish_photo(photo_path, bot, telegram_chat_id):
    with open(photo_path, 'rb') as photo:
        bot.send_photo(chat_id=telegram_chat_id, photo=photo)
        print(f"Фото опубликовано {photo_path}")


def execution_main_logic(publish_delay, bot, telegram_chat_id, pars_directory, max_file_size_mb):
    photo_list = get_photo_list(pars_directory)
    random.shuffle(photo_list)
    
    while True:
        for photo_path in photo_list:
            if scan_file_size(photo_path, max_file_size_mb):
                publish_photo(photo_path, bot, telegram_chat_id)
                time.sleep(publish_delay)
            else:
                print(f"Пропущено из-за размера: {photo_path}")
        random.shuffle(photo_list)


def main():
    load_dotenv()
    
    telegram_bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    telegram_chat_id = os.getenv('TELEGRAM_CHAT_ID')
    pars_directory = os.getenv('PARS_DIRECTORY', default=os.getcwd())
    max_file_size_mb = 20
    
    
    bot = telegram.Bot(token=telegram_bot_token)
    
    parser = argparse.ArgumentParser(description="Запуск бота для отправки фото в мессенджер Телеграм")
    parser.add_argument("-publish_delay", 
                        type=int, 
                        default=14400, 
                        help="Задержка времени перед отправкой фотографии (стандартное значение 4 часа: 14400 секунд)")
    args = parser.parse_args()
    
    execution_main_logic(args.publish_delay, bot, telegram_chat_id, pars_directory, max_file_size_mb)
    
    
if __name__ == "__main__":
    main()    