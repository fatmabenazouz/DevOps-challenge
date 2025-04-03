from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def send_booking_confirmation_email(booking):
    """
    Send a booking confirmation email to the user
    """
    subject = f'Booking Confirmation - {booking.class_schedule.fitness_class.title}'
    
    context = {
        'booking': booking,
        'user': booking.user,
        'class_schedule': booking.class_schedule,
        'fitness_class': booking.class_schedule.fitness_class,
    }
    
    html_message = render_to_string('bookings/email/booking_confirmation.html', context)
    plain_message = strip_tags(html_message)
    
    send_mail(
        subject,
        plain_message,
        settings.DEFAULT_FROM_EMAIL,
        [booking.user.email],
        html_message=html_message,
        fail_silently=False,
    )

def send_booking_cancellation_email(booking):
    """
    Send a booking cancellation email to the user
    """
    subject = f'Booking Cancelled - {booking.class_schedule.fitness_class.title}'
    
    context = {
        'booking': booking,
        'user': booking.user,
        'class_schedule': booking.class_schedule,
        'fitness_class': booking.class_schedule.fitness_class,
    }
    
    html_message = render_to_string('bookings/email/booking_cancellation.html', context)
    plain_message = strip_tags(html_message)
    
    send_mail(
        subject,
        plain_message,
        settings.DEFAULT_FROM_EMAIL,
        [booking.user.email],
        html_message=html_message,
        fail_silently=False,
    )

def send_class_reminder_email(booking):
    """
    Send a reminder email to the user about their upcoming class
    """
    subject = f'Reminder: {booking.class_schedule.fitness_class.title} Class Tomorrow'
    
    context = {
        'booking': booking,
        'user': booking.user,
        'class_schedule': booking.class_schedule,
        'fitness_class': booking.class_schedule.fitness_class,
    }
    
    html_message = render_to_string('bookings/email/class_reminder.html', context)
    plain_message = strip_tags(html_message)
    
    send_mail(
        subject,
        plain_message,
        settings.DEFAULT_FROM_EMAIL,
        [booking.user.email],
        html_message=html_message,
        fail_silently=False,
    )
    
    # Mark reminder as sent
    booking.reminder_sent = True
    booking.save(update_fields=['reminder_sent'])