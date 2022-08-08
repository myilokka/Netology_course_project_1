import logging
from DiskStrategy import YandexDiskStrategy
from VK import VK

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        filename='logs.log',
                        format="%(asctime)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s",
                        datefmt='%H:%M:%S')

    vk_token =  input('Введите токен для ВК: ')
    ya_token = input('Введите токен для ЯндексДиск: ')
    owner_id = input('Введите id профиля ВК: ')
    count = input('Введите количество сохраняемых фото: ')
    yandex = YandexDiskStrategy(ya_token)
    yandex.upload_photos(owner_id, count, vk_token)
