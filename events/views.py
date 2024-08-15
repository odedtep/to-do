from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .models import Location, Event, EventCategory, CartItem
from django.contrib.auth.decorators import login_required
from .forms import EventForm

def index(request):
    locations = Location.objects.all()
    return render(request, 'index.html', {'locations': locations})


def location_detail(request, location_id):
    location = get_object_or_404(Location, id=location_id)
    activities = Event.objects.filter(location=location)
    return render(request, 'location_detail.html', {'location': location, 'activities': activities})


def events(request):
    location_id = request.GET.get('location')
    date = request.GET.get('date')

    events = Event.objects.all()

    if location_id:
        events = events.filter(location_id=location_id)

    if date:
        events = events.filter(start_date=date)

    return render(request, 'events.html', {'events': events})



@login_required
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.creator = request.user
            event.save()
            form.save_m2m()
            return redirect('events')
    else:
        form = EventForm()
    return render(request, 'create_event.html', {'form': form})


# need to add a msg if event created successfully


@login_required
def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.method == 'POST' and request.user.is_authenticated:
        if event.payment_type == Event.PAY_TO_JOIN and event.payment_amount > 0:
            CartItem.objects.get_or_create(event=event, user=request.user)
            return redirect('user_cart')
        elif event.payment_type == Event.PAY_FOR_TASK and request.user == event.creator:
            return redirect('event_detail', event_id=event.id)
        else:
            CartItem.objects.get_or_create(event=event, user=request.user)
            return redirect('user_cart')

    return render(request, 'event_detail.html', {'event': event})

@login_required
def event_view(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request, 'event_view.html', {'event': event})



@login_required
def add_to_cart(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    CartItem.objects.get_or_create(event=event, user=request.user)
    return redirect('user_cart')


@login_required
def user_cart(request):
    cart_items = CartItem.objects.filter(user=request.user).order_by('event__start_date')
    return render(request, 'user_cart.html', {'cart_items': cart_items})



