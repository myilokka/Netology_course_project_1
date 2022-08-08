import requests
import json
from tqdm import tqdm
import logging
from VK import VK


class DiskStrategy:
    def create_folder(self):
        pass

    def upload_photos(self, owner_id, count):
        pass


class YandexDiskStrategy(DiskStrategy):
    def __init__(self, token):
        # self.token = input('Введите токен для ЯндексДиск: ')
        self.token = token
        self.url = 'https://cloud-api.yandex.net/v1/disk/resources'

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)}

    def create_folder(self):
        logging.info('Папка создается.')
        params = {'path': 'vk_photos'}
        headers = self.get_headers()
        res = requests.put(self.url, headers=headers, params=params)
        logging.info('Папка создана.')
        return res

    def upload_photos(self, owner_id, count, vk_token):
        self.create_folder()
        logging.info('Загрузка фото на ЯндексДиск началась.')
        vk = VK(vk_token)
        photos_list = vk.sort_photos(owner_id, count)
        tmp_list = []
        headers = self.get_headers()
        for i in tqdm(photos_list):
            tmp_dict = {'file_name': '{}.jpg'.format(str(i[1])),
                        'size': i[2]}
            tmp_list.append(tmp_dict)
            params = {
                'path': '{}/{}.jpg'.format('vk_photos', str(i[1])),
                'url': i[0]
                }
            response = requests.post(self.url + '/upload', headers=headers, params=params)
            tmp_dict = {}
        logging.info('Загрузка фото на ЯндексДиск закончена.')
        result = json.dumps(tmp_list)
        with open('result.txt', 'w') as file:
            file.write(result)
        return
