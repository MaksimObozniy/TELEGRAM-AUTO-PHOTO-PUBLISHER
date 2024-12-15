import telegram
import argparse
import config
import os
import random
import time


def main(PUBLISH_DELAY):
    
    photo_list = get_photo_list(DERICTORY)
    random.shuffle(photo_list)
    
    while True:
        for photo_path in photo_list:
            publish_photo(photo_path)
            time.sleep(PUBLISH_DELAY)
        random.shuffle(photo_list)


def get_photo_list(directory):
    photos =[]
    for root, _, files in os.walk(directory):
        for filen in files:
            if filen.lower().endswith((".jpg", ".jpeg", ".png")):
                photos.append(os.path.join(root, filen))
    return photos


def publish_photo(photo_path):
    with open(photo_path, 'rb') as photo:
        bot.send_photo(chat_id=TELEGRAM_CHAT_ID, photo=photo)
        print(f"Фото опубликовано {photo_path}")


if __name__ == "__main__":
    argparse = argparse.ArgumentParser(description="Запуск бота для отправки фото в мессенджер Телеграм")
    argparse.add_argument("-PUBLISH_DELAY", type=int, default=14400, help="Задежка времени перед отправкой фотографии (стандартное значение 4 часа: 14400 секунд)")
    args = argparse.parse_args()
    
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN") 
    TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
    DERICTORY = os.getenv("DERICTORY")
    
    bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)
    
    main(args.PUBLISH_DELAY)
    