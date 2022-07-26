import os
import requests
from dotenv import load_dotenv


def count_clicks(token, url):
    auth_headers = {'Authorization': f'Bearer {token}'}
    total_clicks_url = f'https://api-ssl.bitly.com/v4/bitlinks/{url}/clicks/summary'
    response = requests.get(total_clicks_url, params={'units': -1}, headers=auth_headers)
    response.raise_for_status()
    count_clicks = response.json()['total_clicks']
    return count_clicks


def shorten_link(token, url):
    auth_headers = {'Authorization': f'Bearer {token}'}
    payloads = {"long_url": url}
    response = requests.post('https://api-ssl.bitly.com/v4/shorten', json=payloads, headers=auth_headers)
    response.raise_for_status()
    bitlink = response.json()['id']
    return bitlink


def is_bitlink(token, url):
    auth_headers = {'Authorization': f'Bearer {token}'}
    is_bitlink_url = f'https://api-ssl.bitly.com/v4/bitlinks/{url}'
    response = requests.get(is_bitlink_url, headers=auth_headers)
    return response.ok


if __name__ == "__main__":
    load_dotenv()
    token = os.environ['BITLY_TOKEN']
    try:
        some_lurl = str(input("Введите ссылочку: "))
        if is_bitlink(token, some_lurl):
            print("Кликов по ссылке: ", count_clicks(token, some_lurl))
        else:
            print('Битлинк', shorten_link(token, some_lurl))
    except requests.exceptions.HTTPError as exc:
        print(exc)
