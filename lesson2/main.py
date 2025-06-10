import os

import requests

from dotenv import load_dotenv
from urllib.parse import urlparse


class NoStats(Exception):
    """Выбрасывается, когда нет статистики кликов."""
    pass


def create_exception(error_msg):
    # Создает класс для ошибок получаемых от VK.
    #
    # Срезает ключевые слова для создания класса соответсвующего PEP 8.
    if ':' in error_msg:
        cls_name = error_msg.split(': ')[1].title().replace(' ', '')
    else:
        cls_name = error_msg.title().replace(' ', '')
    
    global exception_cls  # Позволяет вызывать созданный класс в Исключениях
    exception_cls = type(cls_name, (Exception,), {})
    globals()[cls_name] = exception_cls

    return exception_cls


def is_shorten_link(url):
    parsed = urlparse(url)
    url_netloc = parsed.netloc

    if url_netloc == 'vk.cc':
        return True
    return False


def shorten_link(token, url):
    headers = {
        'Authorization': 'Bearer {token}'.format(token=token)
    }

    parameters = {'private': 0, 'url': url, 'v': '5.199'}
    method_url = 'https://api.vk.com/method/utils.getShortLink'
    response = requests.get(method_url, params=parameters, headers=headers)
    response.raise_for_status()

    data = response.json()
    if 'error' in data:
        error_msg = data['error']['error_msg']

        raise create_exception(error_msg)(error_msg)

    short_link = data['response']['short_url']
    return short_link


def count_clicks(token, short_link):
    parsed = urlparse(short_link)
    url_path = parsed.path[1:]
    headers = {
        'Authorization': 'Bearer {token}'.format(token=token)
    }

    parameters = {'extended': 0, 'key': url_path, 'v': '5.199'}
    method_url = 'https://api.vk.com/method/utils.getLinkStats'
    response = requests.get(method_url, params=parameters, headers=headers)
    response.raise_for_status()
    data = response.json()
    if 'error' in data:
        error_msg = data['error']['error_msg']

        raise create_exception(error_msg)(error_msg)
    if data['response']['stats'] == []:
        raise NoStats('No one clicked on the link: no data found')
    clicks_count = data['response']['stats'][0]['views']
    return clicks_count


def main():
    load_dotenv()
    vk_token = os.environ['vk_token']

    link = input('Введите ссылку: ')
    if not is_shorten_link(link):
        try:
            short_link = shorten_link(vk_token, link)
            print('Сокращенная ссылка: ', short_link)
        except requests.exceptions.ConnectionError as error:
            print(f'Connection error: {error}')
        except requests.exceptions.HTTPError as error:
            print(f'Request failed: {error}')
        except exception_cls as error:
            print(f'An error occurred. {error}')
    else:
        try:
            clicks_count = count_clicks(vk_token, link)
            print('Количество кликов по ссылке:', clicks_count)
        except NoStats as error:
            print(f'An error occurred. {error}')
        except exception_cls as error:
            print(f'An error occurred. {error}')


if __name__ == '__main__':
    main()
