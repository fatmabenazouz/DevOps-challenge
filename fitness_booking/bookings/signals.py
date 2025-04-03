from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Booking
from .emails import send_booking_confirmation_email

@receiver(post_save, sender=Booking)
def handle_new_booking(sender, instance, created, **kwargs):
    """
    Signal to automatically send confirmation email when a booking is created
    """
    if created and instance.status == 'confirmed':
        send_booking_confirmation_email(instance)