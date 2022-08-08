import requests
import logging
import json


class VK:
    def __init__(self, token):
        self.token = token

    def get_photos(self, owner_id, count=5):
        url = "https://api.vk.com/method/photos.get"
        album = input("Откуда вы хотите получить фото? 1 - из профиля, 2 - фото со стены, 3 - сохраненные фото. Введите цифру: ")
        album_id = 'profile'
        if album == 1:
            album_id = 'profile'
        elif album == 2:
            album_id = 'wall'
        elif album == 3:
            album_id = 'saved'
        logging.info('Выгрузка фото из Вконтакте началась.')
        params = {'owner_id': owner_id,
                  'extended': '1',
                  'photo_sizes': '1',
                  'count': count,
                  'album_id': album_id,
                  'access_token': self.token,
                  'v': '5.131'}
        res = requests.get(url=url, params=params)
        logging.info('Выгрузка закончена.')
        return res

    def sort_photos(self, owner_id, count):
        tmp_list = []
        photo_list = []
        res = self.get_photos(owner_id, count)
        for item in res.json()['response']['items']:
            for j in item['sizes']:
                if j['type'] == 'w':
                    tmp_list.append(j['url'])
                    tmp_list.append(item['likes']['count'])
                    tmp_list.append('w')
                    break
                if j['type'] == 'x':
                    tmp_list.append(j['url'])
                    tmp_list.append(item['likes']['count'])
                    tmp_list.append('x')
            photo_list.append(tmp_list)
            tmp_list = []
        logging.info('Фото отсортированы.')
        return photo_list
