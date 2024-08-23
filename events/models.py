from django.db import models
from django.contrib.auth.models import User


class Location(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class EventCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class Event(models.Model):
    PUBLIC = 'public'
    PRIVATE = 'private'
    EVENT_VISIBILITY_CHOICES = [
        (PUBLIC, 'Public'),
        (PRIVATE, 'Private (Specific Users)'),
    ]

    PAY_TO_JOIN = 'pay_to_join'
    PAY_FOR_TASK = 'pay_for_task'
    NO_PAYMENT = 'no_payment'
    PAYMENT_TYPE_CHOICES = [
        (PAY_TO_JOIN, 'Participants Pay to Join'),
        (PAY_FOR_TASK, 'Creator Pays Participants'),
        (NO_PAYMENT, 'No Payment'),
    ]

    category = models.ForeignKey(EventCategory, on_delete=models.CASCADE, blank=True, null=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    image = models.ImageField(upload_to='event_images', blank=True, null=True)
    video = models.FileField(upload_to='event_videos', blank=True, null=True)
    invited_users = models.ManyToManyField(User, related_name='invited_events', blank=True)
    visibility = models.CharField(max_length=10, choices=EVENT_VISIBILITY_CHOICES, default=PUBLIC)
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPE_CHOICES, default=NO_PAYMENT)
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0)
    participants = models.ManyToManyField(User, related_name='participated_events', blank=True)

    def __str__(self):
        return self.title if self.title else "Unnamed Event"


class CartItem(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    event = models.ForeignKey(Event, on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ticketmaster_event_id = models.CharField(max_length=255, blank=True, null=True)
    ticketmaster_event_url = models.URLField(blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)  # Add this line to store image URL for Ticketmaster events
    location = models.CharField(max_length=255, blank=True, null=True)  # Add this line to store location
    start_date = models.DateField(blank=True, null=True)  # Add this line to store the event date
    added_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        if self.event:
            return f"{self.event.title} added by {self.user.username}"
        else:
            return f"Ticketmaster Event {self.ticketmaster_event_id} added by {self.user.username}"