import requests
from urllib.parse import urlencode

def get_file(public_key):
    base_url = 'https://cloud-api.yandex.net/v1/disk/public/resources/download?'
    return requests.get(requests.get(base_url + urlencode(dict(public_key=public_key))).json()['href']).content

def install(public_key, file = 'downloaded_file.zip'):

    with open(file, 'wb') as f:
        f.write(get_file(public_key))