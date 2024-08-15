from django.shortcuts import render
import requests

def weather_view(request):
    api_key = 'YOUR_API_KEY'
    city = request.GET.get('city', 'Tallinn')  # Default city if none is provided
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

    return render(request, 'weather.html', context)