from django.urls import path
from .views import delete_event_from_cart
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('home/', views.index, name='home'),
    path('events/', views.all_events, name='all_events'),
    path('create_event/', views.create_event, name='create_event'),
    path('event/<int:event_id>/', views.event_detail, name='event_detail'),
    path('event/<int:event_id>/view/', views.event_view, name='event_view'),
    path('event/<int:event_id>/add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.user_cart, name='user_cart'),
    path('ticketmaster_event/<str:ticketmaster_event_id>/', views.ticketmaster_event_detail, name='ticketmaster_event_detail'),
    path('ticketmaster_event/<str:ticketmaster_event_id>/add_to_cart/', views.add_to_cart_ticketmaster, name='add_to_cart_ticketmaster'),
    path('event/<int:event_id>/delete/', delete_event_from_cart, name='delete_event_from_cart'),
    path('event/delete/<int:event_id>/', views.delete_event, name='delete_event'),


]

