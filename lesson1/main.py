import requests


def get_weather(city):
    payload = {'lang': 'ru', 'nTqM': ''}
    url_template = 'https://wttr.in/{}'
    url = url_template.format(city)
    response = requests.get(url, params=payload)
    response.raise_for_status()

    return response.text


def main():
    places = ["Череповец", "Лондон", "аэропорт Шереметьево"]

    for city in places:
        print(get_weather(city))


if __name__ == "__main__":
    main()
