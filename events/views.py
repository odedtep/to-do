import requests
from django.shortcuts import render, redirect, get_object_or_404
from .models import Location, Event, CartItem
from django.contrib.auth.decorators import login_required
from .forms import EventForm
from django.conf import settings
from django.http import JsonResponse
from django.contrib import messages
from .weather_context import weather_context


def index(request):
    if 'weather_location' in request.session:
        del request.session['weather_location']
    locations = Location.objects.all()
    return render(request, 'index.html', {'locations': locations})


def location_detail(request, location_id):
    location = get_object_or_404(Location, id=location_id)
    activities = Event.objects.filter(location=location)
    return render(
        request,
        'location_detail.html',
        {'location': location, 'activities': activities}
    )


def all_events(request):
    location_id = request.GET.get('location')
    date = request.GET.get('date')

    if location_id:
        weather_location = Location.objects.filter(id=location_id).first()
        if weather_location:
            weather_location = weather_location.name
            request.session['weather_location'] = weather_location
        else:
            weather_location = 'Tallinn'
    else:
        weather_location = request.session.get('weather_location', 'Tallinn')

    events = Event.objects.all()

    if location_id:
        events = events.filter(location__name=weather_location)

    if date:
        events = events.filter(start_date=date)

    weather = weather_context(request, weather_location)

    return render(request, 'events.html', {'events': events, **weather})


@login_required
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.creator = request.user
            event.save()
            form.save_m2m()
            messages.success(request, 'Your event has been created!')
            return redirect('all_events')
    form = EventForm()
    return render(request, 'create_event.html', {'form': form})


# @login_required
def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    location_name = event.location.name \
        if event.location \
        else 'Tallinn'

    if event.location:
        request.session['weather_location'] = event.location.name

    weather = weather_context(request, location_name)

    participants = event.participants.count()
    if request.method == 'POST' and request.user.is_authenticated:
        if event.payment_type == Event.PAY_TO_JOIN and event.payment_amount > 0:
            CartItem.objects.get_or_create(event=event, user=request.user)
            return redirect('user_cart')
        elif event.payment_type == Event.PAY_FOR_TASK and request.user == event.creator:
            return redirect('event_detail', event_id=event.id)
    return render(request, 'event_detail.html',
                  {'event': event,
                   'participants': participants,
                   **weather})


@login_required
def event_view(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request, 'event_view.html', {'event': event})


@login_required
def add_to_cart(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if not request.user in event.participants.all():
        event.participants.add(request.user)
    CartItem.objects.create(event=event, user=request.user)
    return redirect('user_cart')


@login_required
def user_cart(request):
    cart_items = CartItem.objects.filter(user=request.user).order_by('event__start_date')
    return render(request, 'user_cart.html', {'cart_items': cart_items})


def get_ticketmaster_events(request, city):
    url = 'https://app.ticketmaster.com/discovery/v2/events.json'
    params = {
        'apikey': settings.TICKETMASTER_API_KEY,
        'city': city,
        'size': 10
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        events_data = data.get('_embedded', {}).get('events', [])

        filtered_events = []
        for event in events_data:
            # Extract the required fields
            event_name = event.get('name')
            images = event.get('images', [])
            third_image_url = images[2].get('url') if len(images) > 2 else None
            start_date = event.get('dates', {}).get('start', {}).get('localDate')
            start_time = event.get('dates', {}).get('start', {}).get('localTime')
            venue_info = event.get('_embedded', {}).get('venues', [{}])[0]
            venue_name = venue_info.get('name')
            city_name = venue_info.get('city', {}).get('name')
            address_line1 = venue_info.get('address', {}).get('line1')
            longitude = venue_info.get('location', {}).get('longitude')
            latitude = venue_info.get('location', {}).get('latitude')

            # Create a new event dictionary
            filtered_event = {
                'name': event_name,
                'image_url': third_image_url,
                'start_date': start_date,
                'start_time': start_time,
                'city_name': city_name,
                'address_line1': address_line1,
                'longitude': longitude,
                'latitude': latitude,
                'venue': venue_name
            }
            filtered_events.append(filtered_event)

        return JsonResponse(filtered_events, safe=False)
    else:
        return JsonResponse({'error': 'Failed to fetch data from Ticketmaster API'}, status=response.status_code)
