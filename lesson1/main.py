import requests


CHEREPOVETS = "Череповец"
LONDON = "Лондон"
SHEREMETYEVO_AP = "аэропорт Шереметьево"


def weather(city):
    payload = {'lang': 'ru', 'nTqM': ''}
    url_template = 'https://wttr.in/{}'
    url = url_template.format(city)
    response = requests.get(url, params=payload)
    response.raise_for_status()

    return response.text


if __name__ == "__main__":
    print(weather(CHEREPOVETS))
    print(weather(LONDON))
    print(weather(SHEREMETYEVO_AP))
