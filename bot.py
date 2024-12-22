import telegram
import argparse
import os
import random
import time


TELEGRAM_BOT_TOKEN = os.environ['TELEGRAM_BOT_TOKEN'] 
TELEGRAM_CHAT_ID = os.environ['TELEGRAM_CHAT_ID']
PARS_DIRECTORY = os.getenv('PARS_DIRECTORY', default=os.getcwd())
MAX_FILE_SIZE_MB = 20

def get_photo_list():
    
    photos =[]
    for root, _, files in os.walk(PARS_DIRECTORY):
        for filen in files:
            if filen.lower().endswith((".jpg", ".jpeg", ".png")):
                photos.append(os.path.join(root, filen))
    return photos

def file_size_scan(photo_path):
    file_size = os.path.getsize(photo_path) / (1024 * 1024)
    
    if file_size > MAX_FILE_SIZE_MB:
        return False
    return True
    
    
def publish_photo(photo_path, bot):
    with open(photo_path, 'rb') as photo:
        bot.send_photo(chat_id=TELEGRAM_CHAT_ID, photo=photo)
        print(f"Фото опубликовано {photo_path}")


def main_logic(pubilsh_delay, bot):
    photo_list = get_photo_list()
    random.shuffle(photo_list)
    
    while True:
        for photo_path in photo_list:
            publish_photo(photo_path, bot)
            time.sleep(pubilsh_delay)
        random.shuffle(photo_list)


def main():
    bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)
    
    parser = argparse.ArgumentParser(description="Запуск бота для отправки фото в мессенджер Телеграм")
    parser.add_argument("-pubilsh_delay", type=int, default=14400, help="Задержка времени перед отправкой фотографии (стандартное значение 4 часа: 14400 секунд)")
    args = parser.parse_args()
    
    main_logic(args.pubilsh_delay, bot)
    
    
if __name__ == "__main__":
    main()    