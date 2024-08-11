from django.urls import path

from events import views

urlpatterns = [
    path('', views.index, name='index'),
    path('events/', views.events, name='events'),
    path('create_event/', views.create_event, name='create_event'),
]