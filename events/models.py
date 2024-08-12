from django.db import models
from django.contrib.auth.models import User


class Location(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


# class UserProfile(models.Model):
#     first_name = models.CharField(max_length=100)
#     surname = models.CharField(max_length=100)
#     email = models.EmailField()
#     phone = models.CharField(max_length=100)
#     location = models.ForeignKey(Location, on_delete=models.CASCADE)
#
#     def __str__(self):
#         return self.first_name

class EventCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class Event(models.Model):
    category = models.ForeignKey(EventCategory, on_delete=models.CASCADE,blank=True, null=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE,blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE,blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)  # can be optional
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)  # can be optional
    invited_users = models.ManyToManyField(User, related_name='invited_events', blank=True, null=True)

    # public or private

    def __str__(self):
        return self.name


class CartItem(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    event = models.ForeignKey(Event, on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return f"{self.event.title} added by {self.user.username}"
