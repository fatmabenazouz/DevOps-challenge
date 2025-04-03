from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['user', 'class_schedule', 'status', 'booking_date', 'reminder_sent']
    list_filter = ['status', 'booking_date', 'class_schedule__fitness_class__category']
    search_fields = ['user__username', 'user__email', 'class_schedule__fitness_class__title']
    date_hierarchy = 'booking_date'
    readonly_fields = ['booking_date']