import datetime
from django.core.management.base import BaseCommand
from django.utils import timezone
from bookings.models import Booking
from bookings.emails import send_class_reminder_email

class Command(BaseCommand):
    help = 'Send reminder emails for upcoming classes'

    def handle(self, *args, **kwargs):
        tomorrow = timezone.now().date() + datetime.timedelta(days=1)
        tomorrow_min = datetime.datetime.combine(tomorrow, datetime.time.min, tzinfo=timezone.get_current_timezone())
        tomorrow_max = datetime.datetime.combine(tomorrow, datetime.time.max, tzinfo=timezone.get_current_timezone())
        
        bookings = Booking.objects.filter(
            status='confirmed',
            reminder_sent=False,
            class_schedule__start_time__range=(tomorrow_min, tomorrow_max),
            class_schedule__is_cancelled=False
        )
        
        count = 0
        for booking in bookings:
            send_class_reminder_email(booking)
            count += 1
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully sent {count} class reminder emails')
        )