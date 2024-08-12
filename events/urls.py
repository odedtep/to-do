from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='events'),
    path('events/', views.events, name='events'),
    path('create_event/', views.create_event, name='create_event'),
    path('event/<int:event_id>/', views.event_detail, name='event_detail'),
    path('event/<int:event_id>/add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.user_cart, name='user_cart'),
]