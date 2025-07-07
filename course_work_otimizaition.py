import json
from token_yandex import token_yand
import requests
from tqdm import tqdm
import time


class Doge:
    def __init__(self, token_yd):
        self.base_url = "https://cloud-api.yandex.net/v1/disk/"
        self.url_breed_list = "https://dog.ceo/api/breeds/list/all"
        self.dogs_dict = requests.get(self.url_breed_list).json().get("message", {})
        self.token_yd = token_yd
        self.headers = {"Authorization": f"{self.token_yd}"}
        self.uploaded_files = []


    def created_list_breed(self):
        """
         A function for getting a file with a list of dog breeds and sub breeds
        """

        with open('list breed and sub breed dogs.txt', "w") as f:
            for breed, sub_breed in self.dogs_dict.items():
                f.write(f"{breed} - {', '.join(sub_breed) if sub_breed != [] else "miss"}\n")


    def find_breed_dog(self, breed_name):
        """
        A function for detecting the presence of a breed in the list
        :param breed_name:
        :return:
        """
        if breed_name in self.dogs_dict:
            print(f"\nПорода {breed_name} найдена.")
            return breed_name
        raise ValueError (f'Порода "{breed_name}" не найдена в списке.')


    def find_sub_breed_dog(self, sub_breed_name):
        """
        a function for detecting the presence of a sub-breed in the list
        :param sub_breed_name:
        :return:
        """
        for breed, sub_breed in self.dogs_dict.items():
            if sub_breed_name in sub_breed:
                print(f'У породы "{breed}" найдена подпорода "{sub_breed_name}".')
                return sub_breed_name
        raise ValueError (f'Подпорода "{sub_breed_name}" не найдена в списке.')

    def created_folder(self, path):
        """
        A function for creating a folder
        :param path:
        """
        url_disk = f"{self.base_url}resources"
        params = {"path": f'{path}'}
        response = requests.put(url_disk, params=params, headers=self.headers)
        if 200 <= response.status_code < 300:
            print(f'Папка {path} создана.')
        elif 400 <= response.status_code < 500:
            print(f'Папка {path} уже существует')
        else:
            print(f'Ошибка при создании {path}: {response.status_code}, {response.text}')


    def create_folders_for_breed_and_sub_breed(self, breed_name, sub_breed=None):
        """
        A function for creating breed folders, and if there is a sub_breed,
         creates a folder inside the breed folder sub_breed.
        :param breed_name:
        :param sub_breed:
        :return:
        """
        breed_name = self.find_breed_dog(breed_name)
        self.created_folder(f'Dogs/{breed_name}')
        if sub_breed is not None:
            sub_breed_name = self.find_sub_breed_dog(sub_breed)
            self.created_folder(f'Dogs/{breed_name}/{sub_breed_name}/')


    def upload_image(self, image_url, folder_path, file_name):
        """
        A function for uploading images to a folder on yandex.disk
        :param image_url:
        :param folder_path:
        :param file_name:
        :return:
        """
        url_upload = f"{self.base_url}resources/upload"
        params = {
            "url": image_url,
            "path": f"{folder_path}/{file_name}"
        }
        response = requests.post(url_upload, params=params, headers=self.headers)
        self.uploaded_files.append({"file_name": file_name})


    def upload_images_folder(self, breed_name, sub_breed=None):
        """
        The main function is to create a folder and
        upload images of specified breeds and sub-breeds.
        :param breed_name:
        :param sub_breed:
        :return:
        """
        folder_path = f"Dogs/{breed_name}"
        if sub_breed is not None:
            folder_path = f"Dogs/{breed_name}/{sub_breed}"
        self.create_folders_for_breed_and_sub_breed(breed_name, sub_breed)

        url_images = f"https://dog.ceo/api/breed/{breed_name}/images/random/5"
        if sub_breed is not None:
            url_images = f"https://dog.ceo/api/breed/{breed_name}/{sub_breed}/images/random/2"

        response = requests.get(url_images)

        images = response.json().get("message", [])
        with tqdm(images, desc=f'Загрузка изображений для {breed_name}/'
                               f'{sub_breed if sub_breed else breed_name}', unit=" изображений") as pbar:
            for image_url in pbar:
                file_name = f'{image_url.split('/')[-1]}-{breed_name}'
                self.upload_image(image_url, folder_path, file_name)
                time.sleep(0.1)
        self.save_uploaded_files_to_json()


    def save_uploaded_files_to_json(self):
        """ function for saving a json file"""
        with open("uploaded_files.json","w",encoding="utf-8") as json_file:
            json.dump(self.uploaded_files, json_file, ensure_ascii=False, indent=2)


    def upload_all_images(self):
        total_items = sum(len(sub_breeds) + 1 for sub_breeds in self.dogs_dict.values())
        with tqdm(total=total_items, desc="Загрузка всех изображений", unit=f" пород/подпород")as pbar:
            for breed, sub_breed in self.dogs_dict.items():
                if sub_breed:
                    for sb in sub_breed:
                        self.upload_images_folder(breed, sb)
                        pbar.update(1)
                else:
                    self.upload_images_folder(breed)
                    pbar.update(1)
        self.save_uploaded_files_to_json()
