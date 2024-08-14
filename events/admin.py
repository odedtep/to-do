from django.contrib import admin
from .models import Location, EventCategory, Event


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(EventCategory)
class EventCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'start_date', 'end_date', 'location', 'category',
        'creator', 'visibility', 'payment_type', 'payment_amount',
    )
    list_filter = ('visibility', 'payment_type', 'location', 'category')
    search_fields = ('title', 'description')
    date_hierarchy = 'start_date'
