from token_yandex import token_yand
import requests
from pprint import pprint

url = "https://dog.ceo/api/breeds/list/all"
dogs = requests.get(url).json()# Получаем словарь пород


dogs = dogs["message"]#Оставляем только породы, и подпороды
for dog, under_dog in dogs.items():# Перебираем dog - породы, under_dog - подпороды
    if dog in dogs and under_dog != []: # если порода есть в в списке пород и подпороды не равны пустому списку
        url_disk = "https://cloud-api.yandex.net/v1/disk/resources"
        params = {
            "path": f"Dogs/{dog}"
        }
        headers = {
            "Authorization": f"{token_yand}"
        }
        response = requests.put(url_disk, params=params, headers=headers)#Создаем папку для пород собак
        for u_dog in under_dog:# перебираем все подпороды
            url_path_disk = f"https://cloud-api.yandex.net/v1/disk/resources/"
            params = {
                "path": f"Dogs/{dog}/{u_dog}"
            }
            headers = {
                "Authorization": f"{token_yand}"
            }
            response = requests.put(url_path_disk, params=params, headers=headers)
            url_dogs = f"https://dog.ceo/api/breed/{dog}/{u_dog}/images/random/1"
            doge = requests.get(url_dogs).json()
            doge = doge["message"]#Оставляем только список с сcылкой
            doge = "".join(doge)#Преобразуем список к строке, так как в списке всего 1 элемент
            print(doge)
            doge_url = doge.split("/")#вытаскиваем имя файла
            print(doge_url[-2])

            print(dog)
            url_yand_upload = "https://cloud-api.yandex.net/v1/disk/resources/upload"
            params = {
                "url": f"{doge}",
                "path": f"Dogs/{dog}/{u_dog}/{u_dog}{doge_url[-1]}"
            }
            response = requests.post(url_yand_upload, params=params,
                                     headers=headers)
    else:
        url_disk = "https://cloud-api.yandex.net/v1/disk/resources"
        params = {
            "path": f"Dogs/{dog}"
        }
        headers = {
            "Authorization": f"{token_yand}"
        }
        response = requests.put(url_disk, params=params, headers=headers)
        url_dogs = f"https://dog.ceo/api/breed/{dog}/images/random/10"
        doge = requests.get(url_dogs).json()
        doge = doge["message"]
        for dog_url in doge:
            url_yand_upload = "https://cloud-api.yandex.net/v1/disk/resources/upload"
            dog_name_url = dog_url.split("/")
            params = {
                "url": f"{dog_url}",
                "path": f"Dogs/{dog}/{dog}{dog_name_url[-1]}"
            }
            response = requests.post(url_yand_upload, params=params,
                                     headers=headers)
            print(dog_url)
