import requests


def weather_context(request):
    api_key = '2d6b166ad4a337b949d2e1b86f2bde69'
    city = 'Tallinn'
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'

    try:
        response = requests.get(url)
        weather_data = response.json()

        context = {
            'city': city,
            'temperature': weather_data['main']['temp'],
            'description': weather_data['weather'][0]['description'],
            'icon': weather_data['weather'][0]['icon'],
        }
    except (requests.exceptions.RequestException, KeyError):
        context = {
            'city': city,
            'temperature': 'N/A',
            'description': 'N/A',
            'icon': 'N/A',
        }

    return context
