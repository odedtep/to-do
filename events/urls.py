from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('events/', views.events, name='events'),
    path('create_event/', views.create_event, name='create_event'),
    path('event/<int:event_id>/', views.event_detail, name='event_detail'),
    path('event/<int:event_id>/view/', views.event_view, name='event_view'),
    path('event/<int:event_id>/add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.user_cart, name='user_cart'),
    path('ticketmaster/<str:city>/', views.get_ticketmaster_events, name='ticketmaster-city')
]

