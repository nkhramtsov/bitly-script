import os
import requests
from urllib.parse import urlparse

API_BITLY_URL = 'https://api-ssl.bitly.com/v4/bitlinks/'


def shorten_link(token, url):

    headers = {'Authorization': f'Bearer {token}'}
    payload = {'long_url': url}

    response = requests.post(API_BITLY_URL, headers=headers, json=payload)
    response.raise_for_status()

    bitlink = response.json()['link']

    return bitlink


def count_clicks(token, link):

    parsed_link = urlparse(link)
    headers = {'Authorization': f'Bearer {token}'}
    payload = {'unit': 'day', 'units': -1}

    response = requests.get(
        f'{API_BITLY_URL}'
        f'{parsed_link.netloc}{parsed_link.path}/clicks/summary',
        headers=headers, params=payload)
    response.raise_for_status()

    total_clicks = response.json()['total_clicks']

    return total_clicks


def is_bitlink(url):

    parsed_url = urlparse(url)

    response = requests.get(
        f'{API_BITLY_URL}{parsed_url.netloc}{parsed_url.path}')

    return response.ok

if __name__ == "__main__":

    TOKEN = os.environ['BITLY_TOKEN']
    print('Введите ссылку')
    inputed_url = input()

    try:
        if is_bitlink(inputed_url):
            total_clicks = count_clicks(TOKEN, inputed_url)
            print('Кликов', total_clicks)
        else:
            bitlink = shorten_link(TOKEN, inputed_url)
            print('Битлинк', bitlink)
    except requests.exceptions.HTTPError:
        print('Ошибка')
