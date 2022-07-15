from dotenv import load_dotenv
import argparse
import os
import requests
from urllib.parse import urlparse
import sys

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
        f'{parsed_link.netloc}/{parsed_link.path}/clicks/summary',
        headers=headers,
        params=payload
    )
    response.raise_for_status()

    total_clicks = response.json()['total_clicks']

    return total_clicks


def is_bitlink(url):
    parsed_url = urlparse(url)

    response = requests.get(
        f'{API_BITLY_URL}{parsed_url.netloc}/{parsed_url.path}'
    )

    return response.ok


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('link', type=str)

    return parser.parse_args()


if __name__ == "__main__":
    load_dotenv()
    token = os.getenv('BITLY_TOKEN')
    parser = parse_args()

    try:
        if is_bitlink(parser.link):
            total_clicks = count_clicks(token, parser.link)
            print('Кликов', total_clicks)
        else:
            bitlink = shorten_link(token, parser.link)
            print('Битлинк', bitlink)
    except requests.exceptions.HTTPError:
        print('Ошибка')
