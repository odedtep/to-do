import requests
from django.shortcuts import render, redirect, get_object_or_404
from .models import Location, Event, CartItem
from django.contrib.auth.decorators import login_required
from .forms import EventForm
from django.conf import settings
from django.http import JsonResponse
from django.contrib import messages
from .weather_context import weather_context
from django.views.decorators.http import require_POST


def landing_page(request):
    return render(request, 'landing.html')


def index(request):
    if 'weather_location' in request.session:
        del request.session['weather_location']  # get
    locations = Location.objects.all()
    return render(request, 'index.html', {'locations': locations})


def all_events(request):
    location_id = request.GET.get('location')
    date = request.GET.get('date')
    start_date_iso8601 = ''
    end_date_iso8601 = ''
    events = Event.objects.all()
    if location_id:
        events = events.filter(location_id=location_id)
    if date:
        events = events.filter(start_date=date)
        start_date_iso8601 = f"{date}T00:00:00Z"
        end_date_iso8601 = f"{date}T23:59:59Z"
    city = get_city(location_id)
    filtered_events = get_ticketmaster_events(request, city, start_date_iso8601, end_date_iso8601)

    # weather widget
    if location_id:
        weather_location = Location.objects.filter(id=location_id).first()
        if weather_location:
            weather_location = weather_location.name
            request.session['weather_location'] = weather_location
    weather_location = request.session.get('weather_location', 'Tallinn')
    weather = weather_context(request, weather_location)
    return render(request, 'events.html', {
        'events': events,
        'ticketmaster_events': filtered_events,
        **weather})


# Ticketmaster function
def get_city(location_id):
    if location_id is None:
        return ''
    try:
        location_id = int(location_id)
    except ValueError:
        return ''
    locations = Location.objects.all()
    for location in locations:
        if location.id == location_id:
            city = location.name
    return city


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
def add_to_cart(request, event_id=None):
    if event_id:
        # Handle user-created event
        event = get_object_or_404(Event, id=event_id)
        if not request.user in event.participants.all():
            event.participants.add(request.user)

        if CartItem.objects.filter(event=event, user=request.user).exists():
            messages.success(request, 'This event is already in your favorites.')
        else:
            CartItem.objects.create(event=event, user=request.user)
            messages.success(request, 'Your event has been added to your favorites.')
    else:
        messages.error(request, 'Invalid request.')
    return redirect('user_cart')


@login_required
def user_cart(request):
    cart_items = CartItem.objects.filter(user=request.user).order_by('event__start_date')
    return render(request, 'user_cart.html',
                  {'cart_items': cart_items})


def get_ticketmaster_events(request, city, start_date_iso8601, end_date_iso8601):
    url = 'https://app.ticketmaster.com/discovery/v2/events.json'
    params = {
        'apikey': settings.TICKETMASTER_API_KEY,
        'city': city,
        'startDateTime': start_date_iso8601,
        'endDateTime': end_date_iso8601,
        'size': 100,
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return JsonResponse({'error': str(e)}, status=500)

    if response.status_code == 200:
        data = response.json()
        events_data = data.get('_embedded', {}).get('events', [])
        filtered_events = []
        for event in events_data:
            # Extract the required fields
            event_id = event.get('id')
            name = event.get('name')
            images = event.get('images', [])
            image_url = images[0].get('url') if images else None
            start_date = event.get('dates', {}).get('start', {}).get('localDate')
            start_time = event.get('dates', {}).get('start', {}).get('localTime')
            venue_info = event.get('_embedded', {}).get('venues', [{}])[0]
            venue_name = venue_info.get('name')
            city_name = venue_info.get('city', {}).get('name')
            address_line1 = venue_info.get('address', {}).get('line1')
            event_url = event.get('url')

            filtered_event = {
                'id': event_id,
                'name': name,
                'image_url': image_url,
                'start_date': start_date,
                'start_time': start_time,
                'location': city_name,
                'address_line1': address_line1,
                'venue': venue_name,
                'url': event_url
            }

            filtered_events.append(filtered_event)

        return filtered_events
    else:
        return JsonResponse({'error': 'Failed to fetch data from Ticketmaster API'}, status=response.status_code)


def add_to_cart_ticketmaster(request, ticketmaster_event_id=None):
    if ticketmaster_event_id:
        ticketmaster_event_url = request.GET.get('url')
        name = request.GET.get('name')
        image_url = request.GET.get('image_url')
        location = request.GET.get('location')
        description = request.GET.get('description', 'No description available')
        start_date = request.GET.get('start_date')

        if not name or not ticketmaster_event_url:
            messages.error(request, 'Missing needed event details.')
            return redirect('all_events')

        if CartItem.objects.filter(ticketmaster_event_id=ticketmaster_event_id, user=request.user).exists():
            messages.success(request, 'This event is already in your favorites.')
        else:
            CartItem.objects.create(
                title=name,
                location=location,
                description=description,
                ticketmaster_event_id=ticketmaster_event_id,
                ticketmaster_event_url=ticketmaster_event_url,
                image_url=image_url,
                start_date=start_date,
                user=request.user
            )
            messages.success(request, 'Event has been added to your favorites.')
    else:
        messages.error(request, 'Invalid request.')
    return redirect('user_cart')


def ticketmaster_event_detail(request, ticketmaster_event_id):
    print(f"ticketmaster_event_id received: {ticketmaster_event_id}")
    url = 'https://app.ticketmaster.com/discovery/v2/events/' + ticketmaster_event_id
    params = {'apikey': settings.TICKETMASTER_API_KEY}

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return JsonResponse({'error': str(e)}, status=500)

    if response.status_code == 200:
        event_data = response.json()
        # Weather widget
        venue = event_data['_embedded']['venues'][0]
        city = venue.get('city', {}).get('name', 'Tallinn')
        weather = weather_context(request, location=city)

        event_details = {
            'id': ticketmaster_event_id,
            'name': event_data.get('name'),
            'description': event_data.get('info', 'No description available.'),
            'start_date': event_data['dates']['start'].get('localDate'),  # get
            'start_time': event_data['dates']['start'].get('localTime'),  # get
            'venue': event_data['_embedded']['venues'][0].get('name'),  # get
            'image_url': event_data['images'][0]['url'] if 'images' in event_data and event_data['images'] else None,
            'address': event_data['_embedded']['venues'][0].get('address', {}).get('line1'),  # get
            'city': event_data['_embedded']['venues'][0]['city'].get('name'),  # get
            'url': event_data.get('url'),
        }

        return render(request, 'ticketmaster_event_detail.html', {'event': event_details, **weather})

    return JsonResponse({'error': 'Event not found'}, status=404)


# Function to see the event view from cart
@login_required
def ticketmaster_event_detail_view(request, ticketmaster_event_id):
    url = f'https://app.ticketmaster.com/discovery/v2/events/{ticketmaster_event_id}.json'
    params = {'apikey': settings.TICKETMASTER_API_KEY}

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()

        event_data = response.json()

        event = {
            'id': ticketmaster_event_id,
            'name': event_data.get('name'),
            'description': event_data.get('info', 'No description available.'),
            'start_date': event_data['dates']['start'].get('localDate'),
            'start_time': event_data['dates']['start'].get('localTime'),
            'image_url': event_data['images'][0]['url'] if 'images' in event_data and event_data['images'] else None,
            'venue': event_data['_embedded']['venues'][0].get('name'),
            'address': event_data['_embedded']['venues'][0].get('address', {}).get('line1'),
            'city': event_data['_embedded']['venues'][0]['city'].get('name'),
            'url': event_data.get('url'),
        }
        return render(request, 'ticketmaster_event_detail_view.html', {'event': event})

    except requests.exceptions.RequestException as e:

        return JsonResponse({'error': str(e)}, status=500)


# To delete ticketmaster event from your cart

@login_required
@require_POST
def delete_event_from_cart_ticketmaster(request, ticketmaster_event_id):
    user_cart_item = get_object_or_404(CartItem, user=request.user, ticketmaster_event_id=ticketmaster_event_id)
    user_cart_item.delete()
    messages.success(request, 'The event has been successfully removed from your favorites.')
    return redirect('user_cart')


@login_required
@require_POST
def delete_event_from_cart(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    user_cart_item = get_object_or_404(CartItem, user=request.user, event=event)
    user_cart_item.delete()
    messages.success(request, 'The event has been successfully removed from your favorites.')

    return redirect('user_cart')


@login_required
@require_POST
def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.user != event.creator:
        messages.error(request, "You are not authorized to delete this event.")
        return redirect('event_detail', event_id=event_id)
    event.delete()
    messages.success(request, "The event has been successfully deleted.")
    return redirect('all_events')
