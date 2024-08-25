import requests


def weather_context(request, location='Tallinn'):
    api_key = '2d6b166ad4a337b949d2e1b86f2bde69'
    url = f'https://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric'

    try:
        response = requests.get(url)
        weather_data = response.json()

        context = {
            'city': location,
            'temperature': weather_data['main']['temp'],
            'description': weather_data['weather'][0]['description'],
            'icon': weather_data['weather'][0]['icon'],
            'feels_like': weather_data['main']['feels_like'],
            'wind': weather_data['wind']['speed'],
        }
    except (requests.exceptions.RequestException, KeyError):
        context = {
            'city': location,
            'temperature': 'N/A',
            'description': 'N/A',
            'icon': 'N/A',
            'feels_like': 'N/A',
        }

    return context
