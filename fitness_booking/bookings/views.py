from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db import transaction
from .models import Booking
from classes.models import ClassSchedule
from .forms import BookingFeedbackForm
from .emails import send_booking_confirmation_email

@login_required
def booking_list(request):
    upcoming_bookings = request.user.bookings.filter(
        status='confirmed',
        class_schedule__start_time__gt=timezone.now()
    ).order_by('class_schedule__start_time')
    
    past_bookings = request.user.bookings.filter(
        class_schedule__start_time__lt=timezone.now()
    ).order_by('-class_schedule__start_time')
    
    context = {
        'upcoming_bookings': upcoming_bookings,
        'past_bookings': past_bookings
    }
    
    return render(request, 'bookings/booking_list.html', context)

@login_required
def booking_detail(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    context = {
        'booking': booking
    }
    
    return render(request, 'bookings/booking_detail.html', context)

@login_required
@transaction.atomic
def create_booking(request, schedule_id):
    schedule = get_object_or_404(ClassSchedule, id=schedule_id)
    
    if schedule.start_time <= timezone.now():
        messages.error(request, 'Cannot book a class that has already started or ended.')
        return redirect('schedule_detail', schedule_id=schedule.id)
    
    if schedule.is_cancelled:
        messages.error(request, 'This class has been cancelled.')
        return redirect('schedule_detail', schedule_id=schedule.id)
    
    if schedule.is_full:
        messages.error(request, 'This class is full.')
        return redirect('schedule_detail', schedule_id=schedule.id)
    
    if Booking.objects.filter(user=request.user, class_schedule=schedule).exists():
        messages.error(request, 'You have already booked this class.')
        return redirect('schedule_detail', schedule_id=schedule.id)
    
    booking = Booking.objects.create(
        user=request.user,
        class_schedule=schedule,
        status='confirmed'
    )
    
    schedule.current_capacity += 1
    schedule.save()
    
    send_booking_confirmation_email(booking)
    
    messages.success(request, 'Booking confirmed! Check your email for details.')
    return redirect('booking_detail', booking_id=booking.id)

@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    if booking.class_schedule.start_time <= timezone.now():
        messages.error(request, 'Cannot cancel a booking for a class that has already started or ended.')
        return redirect('booking_detail', booking_id=booking.id)
    
    if request.method == 'POST':
        reason = request.POST.get('reason', '')
        success = booking.cancel(reason)
        
        if success:
            messages.success(request, 'Your booking has been cancelled.')
            return redirect('booking_list')
        else:
            messages.error(request, 'Unable to cancel booking.')
    
    return render(request, 'bookings/cancel_booking.html', {'booking': booking})

@login_required
def submit_feedback(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    if booking.class_schedule.end_time > timezone.now():
        messages.error(request, 'Cannot submit feedback for a class that has not ended yet.')
        return redirect('booking_detail', booking_id=booking.id)
    
    if request.method == 'POST':
        form = BookingFeedbackForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you for your feedback!')
            return redirect('booking_detail', booking_id=booking.id)
    else:
        form = BookingFeedbackForm(instance=booking)
    
    context = {
        'booking': booking,
        'form': form
    }
    
    return render(request, 'bookings/submit_feedback.html', context)