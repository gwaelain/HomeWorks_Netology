import os
import requests

class YaUploader:
    def __init__(self, file_path: str):

        self.file_path = file_path.partition(':')[2]

        self.disk = file_path.partition(':')[0]

        self.full_path = file_path

        self.last_folder = file_path.rpartition('\\')[2]

        for d, dirs, files in os.walk(file_path):
            print(d)
            print(dirs)
            for f in files:
                print(f'Файл для загрузки: {f}')

        print(f'Загружаем файлы на Яндекс.Диск в директорию: /{self.last_folder}')

        self.token = ''
        self.token_prefix= 'OAuth'

    def _get_files_from_folder(self) -> list:

        os.chdir(self.full_path)


        file_list=[]
        for d, dirs, files in os.walk('.'):
            for f in files:
                #file=os.path.abspath(str(f))
                file_list.append(f)


        print(f'Список файлов для загрузки: \n{file_list}')
        return file_list

    def upload(self):
        file_list = self._get_files_from_folder()
        #print(file_list)


        method_get_url = 'GET'
        method_upload_file = 'PUT'
        URL = 'https://cloud-api.yandex.net:443'
        RESOURCE = '/v1/disk/resources/upload'
        headers = {'Authorization': f'{self.token_prefix} {self.token}'}


        for file in file_list:

            params = {'path': f'/{self.last_folder}/{file}'}

            resp = requests.request(method_get_url, URL + RESOURCE, params=params, headers=headers)
            resp_json = resp.json()
            #print(resp_json)

            url_upload = resp_json['href']
            with open(file, "rb") as f:
                up_load = requests.request(method_upload_file, url_upload, data=f, headers=headers)

                #print(up_load)

                if up_load.status_code == 201:
                    print(f'File {file} is successfull uploaded!')
                elif up_load.status_code == 202:
                    print(f'Файл {file} принят сервером, но еще не был перенесен непосредственно в Яндекс.Диск')
                elif up_load.status_code == 412:
                    print(f'При дозагрузке файла {file} был передан неверный диапазон в заголовке Content-Range')
                    return 2
                elif up_load.status_code == 413:
                    print(f'Размер файла {file} превышает 10 ГБ.')
                    return 3
                elif up_load == 413:
                    print(f'Размер файла {file} превышает 10 ГБ.')
                    return 4
                else:
                    print('Some kind error during file {file} upload!')
                    return -1

    def create_folder(self):


        method = 'PUT'
        URL = 'https://cloud-api.yandex.net:443'
        RESOURCE = '/v1/disk/resources'

        params = {'path': f'/{self.last_folder}'}
        headers = {'Authorization': f'{self.token_prefix} {self.token}'}

        resp = requests.request(method, URL + RESOURCE, params=params, headers=headers)
        resp_json = resp.json()
        #print(resp_json)
        if resp.status_code == 201:
            print(f'Папка {self.last_folder} успешно создана!')
            return 0
        elif resp.status_code == 409:
            print(f'Folder {self.last_folder} already exists!')
            return 1
        else:
            print(f'Some kind error during folder {self.last_folder} create!')
            return -1

if __name__ == '__main__':
    target_path=input('Введите путь до папки на компьютере:  ')
    uploader = YaUploader(target_path)
    uploader.create_folder()
    result = uploader.upload()
