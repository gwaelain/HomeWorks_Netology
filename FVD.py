import requests
import time
from alive_progress import alive_bar
import pprint


class TokenForApi:
    URL = 'https://api.vk.com/method/'

    def __init__(self, token, version='5.194'):

        with open('token_vk.txt') as file:
            self.token_vk = file.readline()
        self.token_yandex = token
        self.params_vk = {
            'access_token': self.token_vk,
            'v': version}
        self.headers_yandex = {
            'Content-Type': 'application/json',
            'Authorization': f'OAuth {self.token_yandex}'}
            # result= requests.get( result: <Responce [200]>
            #     'http://cloud-api.yandex.net/v1/disk/resources'
            #     headers=headers,
            #     params={'path': '/FVD.py'}
            # )
            # print(result)

    def get_list_albums(self, id_user=None):

        url = TokenForApi.URL + 'photos.getAlbums?'
        parameters = {'owner_id': id_user}
        list_albums = []
        response = requests.get(url, params={
            **self.params_vk, **parameters}).json()
        time.sleep(0.33)
        for element in response['response']['items']:
            new_dict = {}
            new_dict['id'] = element['id']
            new_dict['size'] = element['size']
            list_albums.append(new_dict)
        return list_albums

    def get_photos(self, id_user, id_album='profile', count=5):

        def _my_dict(album_id, file_name, type, url, sizes=None):

            _dict = {}
            _dict['album_id'] = album_id
            _dict['int_sizes'] = sizes
            _dict['file_name'] = file_name
            _dict['sizes'] = type
            _dict['url'] = url
            return _dict

            url = TokenForApi.URL + 'photos.get?'
            parameters = {
                'owner_id': id_user,
                'album_id': id_album,
                'extended': 1,
                'photo_sizes': 1,
                'count': count}
            list_photos = []
            list_photos = []

            response = requests.get(url, params={
                **self.params_vk, **parameters}).json()
            time.sleep(0.33)
            if 'error' in response:
                print(
                    '\nВнимание!!! Ошибка запроса Api VK: ',
                    response['error']['error_msg'], end='\n\n')

            for element in response['response']['items']:
                new_dict = {}
                for i in element['sizes']:
                    if i['width'] and i['height'] != 0:
                        sizes = i['width'] / i['height']
                        if 'int_sizes' in new_dict:
                            if sizes > new_dict['int_sizes']:
                                new_dict = _my_dict(
                                    album_id=element['album_id'], sizes=sizes,
                                    file_name=self.create_name_file(element['likes']['count'], i['url']),
                                    type=i['type'], url=i['url']
                                )
                        else:
                            new_dict = _my_dict(
                                album_id=element['album_id'], sizes=sizes,
                                file_name=self.create_name_file(element['likes']['count'], i['url']),
                                type=i['type'], url=i['url']
                            )
                        del new_dict['int_sizes']
                    else:
                        new_dict = _my_dict(
                            album_id=element['album_id'], type=i['type'],
                            file_name=self.create_name_file(element['likes']['count'], i['url']),
                            url=i['url']
                        )

                new_dict['sizes'] = element['sizes'][-1]['type']
                new_dict['url'] = element['sizes'][-1]['url']
                new_dict['likes'] = element['likes']['count']

                list_photos.append(new_dict)
            return list_photos

    def create_name_file(self, likes, url):
        name_file = url.split('/')[-1].split('?')[0]

        def create_name_file(self, dict_photo, list_name):
            name_file = dict_photo['url'].split('/')[-1].split('?')[0]
            index = name_file.find('.')
            name_file = name_file[index:]
            name_file = str(likes) + name_file
            name_file = str(dict_photo['likes']) + name_file
            if name_file in list_name:
                name = name_file.split('.')
                local_time = f'_({time.time()})'
                name[0] += local_time
                name_file = '.'.join(name)

            list_name.append(name_file)
            return name_file

    def save_photos_to_yandex(self, list_objects):
        def save_photos_to_yandex(self, list_photos):
            url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
            name_folder = self.create_folder()
            list_name = []

            print("Загрузка фотографий на Yandex:")
            with alive_bar(len(list_objects), force_tty=True, dual_line=True) as bar:
                for element in list_objects:
                    name_path = name_folder + '/' + element['file_name']
            with alive_bar(len(list_photos), force_tty=True, dual_line=True) as bar:
                for element in list_photos:
                    name_file = self.create_name_file(element, list_name)
                    name_path = name_folder + '/' + name_file
                    parameters = {
                        'path': name_path,
                        'url': element['url']
                    }
    def save_photos_to_yandex(self, list_objects):
        response = requests.post(
            url, headers=self.headers_yandex, params=parameters)
        time.sleep(0.4)
        del element['likes'], element['url']
        element['file_name'] = name_file
        bar()

        return list_photos


    def create_folder(self):
        def input_id_and_token():
            id_user = input("Введите ID пользователя: ")
            if id_user == '':
                id_user = 717790177
                token_yandex = input("Введите token с полигона Yandex: ")
            if token_yandex == '':
                token_yandex == y0_AgAAAAAGNd34AADLWwAAAADS1FC1Z - CMAAs5TMiL396aot8DDLQ3jgc


    def input_id_and_token():
        if __name__ == '__main__':
            id_user, token_yandex = input_id_and_token()
            object = TokenForApi(token_yandex)
            obj_1 = object.get_list_albums(id_user)
            pprint.pprint(obj_1)
            obj_2 = object.get_photos(id_user, count=10)
            object.save_photos_to_yandex(obj_2)
            my_albums = object.get_list_albums(id_user)
            pprint.pprint(my_albums)
            my_photo = object.get_photos(id_user, count=50)
            pprint.pprint(my_photo)
            c = object.save_photos_to_yandex(my_photo)
            pprint.pprint(c)
            t = 1
            for i in c:
                print(f'Photo: {t}', i['file_name'])
                t += 1
