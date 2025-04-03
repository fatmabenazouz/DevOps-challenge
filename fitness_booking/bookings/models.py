from django.db import models
from django.contrib.auth.models import User
from classes.models import ClassSchedule

class Booking(models.Model):
    STATUS_CHOICES = [
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('attended', 'Attended'),
        ('no_show', 'No Show'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    class_schedule = models.ForeignKey(ClassSchedule, on_delete=models.CASCADE, related_name='bookings')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='confirmed')
    booking_date = models.DateTimeField(auto_now_add=True)
    cancellation_date = models.DateTimeField(blank=True, null=True)
    cancellation_reason = models.TextField(blank=True, null=True)
    reminder_sent = models.BooleanField(default=False)
    feedback = models.TextField(blank=True, null=True)
    rating = models.PositiveSmallIntegerField(blank=True, null=True)
    
    class Meta:
        unique_together = ['user', 'class_schedule']
        ordering = ['-booking_date']
    
    def __str__(self):
        return f"{self.user.username} - {self.class_schedule}"
    
    def cancel(self, reason=None):
        from django.utils import timezone
        
        if self.status == 'confirmed':
            self.status = 'cancelled'
            self.cancellation_date = timezone.now()
            self.cancellation_reason = reason
            
            self.class_schedule.current_capacity -= 1
            self.class_schedule.save()
            
            self.save()
            
            from bookings.emails import send_booking_cancellation_email
            send_booking_cancellation_email(self)
            
            return True
        return False