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
    list_display = ('title', 'start_date', 'end_date', 'start_time', 'end_time', 'location', 'category', 'creator')
    list_filter = ('start_date', 'end_date', 'location', 'category')
    search_fields = ('title', 'description')
    date_hierarchy = 'start_date'
