import requests
from pprint import pprint
import json
from tqdm import tqdm

class BackupCopying:

    def __init__(self, token_vk, token_ya):
        self.token_vk = token_vk
        self.token_vk = token_ya
        self.url_ya = 'https://cloud-api.yandex.net/v1/disk/resources'

    def get_photos(self, owner_id, count=5):
        url = "https://api.vk.com/method/photos.get"
        params = {'owner_id': owner_id,
                  'extended': '1',
                  'photo_sizes': '1',
                  'count': count,
                  'album_id': 'profile',
                  'access_token': self.token_vk,
                  'v':'5.131'}
        res = requests.get(url=url, params=params)
        # pprint(res.json())
        return res

    def sort_photos(self, owner_id, count=5):
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
        return photo_list

    def ya_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token_ya)}

    def create_folder(self, name_of_folder='vk_photos'):
        params = {'path': name_of_folder}
        headers = self.ya_headers()
        res = requests.put(self.url_ya, headers=headers, params=params)
        return res

    def upload_photos(self, owner_id, count=5,name_of_folder='vk_photos'):
        self.create_folder(name_of_folder)
        photos_list = self.sort_photos(owner_id, count)
        tmp_list = []
        headers = self.ya_headers()
        for i, k in enumerate(tqdm(photos_list)):
                tmp_dict = {'file_name': '{}.jpg'.format(str(photos_list[i][1])),
                            'size': photos_list[i][2]}
                tmp_list.append(tmp_dict)
                params = {
                    'path': '{}/{}.jpg'.format(name_of_folder, str(photos_list[i][1])),
                    'url': photos_list[i][0]
                }
                response = requests.post(self.url_ya + '/upload', headers=headers, params=params)
                tmp_dict = {}
        result = json.dumps(tmp_list)
        return result



if __name__ == '__main__':

    token_ya = input('Введите токен для Яндекс Диска: ')
    token_vk = input('Введите токен для ВК: ')
    owner_id = input('Введите id профиля ВК: ')
    count = input('Введите количество сохраняемых фото: ')

    a = BackupCopying(token_vk, token_ya)
    result1 = a.upload_photos(owner_id, count)
    print(result1)

