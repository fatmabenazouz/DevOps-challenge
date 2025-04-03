from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from unittest.mock import patch

from classes.models import Instructor, ClassCategory, FitnessClass, ClassSchedule
from .models import Booking


class BookingModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )
        
        self.instructor = Instructor.objects.create(
            name="Jane Smith", email="jane@example.com"
        )
        self.category = ClassCategory.objects.create(name="Pilates")
        self.fitness_class = FitnessClass.objects.create(
            title="Core Pilates",
            description="Core strengthening",
            instructor=self.instructor,
            category=self.category,
            duration_minutes=55,
            max_capacity=15,
            difficulty_level="intermediate",
        )
        
        self.start_time = timezone.now() + timedelta(days=1)
        self.end_time = self.start_time + timedelta(minutes=55)
        
        self.schedule = ClassSchedule.objects.create(
            fitness_class=self.fitness_class,
            start_time=self.start_time,
            end_time=self.end_time,
            location="Pilates Studio",
            current_capacity=5,
        )
        
        self.booking = Booking.objects.create(
            user=self.user,
            class_schedule=self.schedule,
            status="confirmed",
        )

    def test_booking_creation(self):
        """Test that a booking can be created properly"""
        self.assertEqual(Booking.objects.count(), 1)
        self.assertEqual(self.booking.user, self.user)
        self.assertEqual(self.booking.class_schedule, self.schedule)
        self.assertEqual(self.booking.status, "confirmed")

    def test_booking_str_representation(self):
        """Test the string representation of the Booking model"""
        expected_str = f"{self.user.username} - {self.schedule}"
        self.assertEqual(str(self.booking), expected_str)

    @patch("bookings.models.send_booking_cancellation_email")
    def test_cancel_method(self, mock_send_email):
        """Test the cancel method of the Booking model"""
        self.assertEqual(self.booking.status, "confirmed")
        self.assertEqual(self.schedule.current_capacity, 5)
        
        result = self.booking.cancel("Testing cancellation")
        
        self.assertTrue(result)
        self.assertEqual(self.booking.status, "cancelled")
        self.assertIsNotNone(self.booking.cancellation_date)
        self.assertEqual(self.booking.cancellation_reason, "Testing cancellation")
        
        self.schedule.refresh_from_db()
        self.assertEqual(self.schedule.current_capacity, 4)
        
        mock_send_email.assert_called_once_with(self.booking)
        
        result = self.booking.cancel()
        self.assertFalse(result)


class BookingViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )
        
        self.instructor = Instructor.objects.create(
            name="Jane Smith", email="jane@example.com"
        )
        self.category = ClassCategory.objects.create(name="Pilates")
        self.fitness_class = FitnessClass.objects.create(
            title="Core Pilates",
            description="Core strengthening",
            instructor=self.instructor,
            category=self.category,
            duration_minutes=55,
            max_capacity=15,
            difficulty_level="intermediate",
        )
        
        self.future_start = timezone.now() + timedelta(days=1)
        self.future_end = self.future_start + timedelta(minutes=55)
        
        self.future_schedule = ClassSchedule.objects.create(
            fitness_class=self.fitness_class,
            start_time=self.future_start,
            end_time=self.future_end,
            location="Pilates Studio",
            current_capacity=5,
        )
        
        self.past_start = timezone.now() - timedelta(days=1)
        self.past_end = self.past_start + timedelta(minutes=55)
        
        self.past_schedule = ClassSchedule.objects.create(
            fitness_class=self.fitness_class,
            start_time=self.past_start,
            end_time=self.past_end,
            location="Pilates Studio",
            current_capacity=5,
        )
        
        self.booking = Booking.objects.create(
            user=self.user,
            class_schedule=self.future_schedule,
            status="confirmed",
        )
        
        self.client.login(username="testuser", password="testpass123")

    def test_booking_list_view(self):
        """Test the booking list view"""
        response = self.client.get(reverse("booking_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "bookings/booking_list.html")
        self.assertContains(response, "Core Pilates")
        
        self.assertEqual(len(response.context["upcoming_bookings"]), 1)
        self.assertEqual(len(response.context["past_bookings"]), 0)

    def test_booking_detail_view(self):
        """Test the booking detail view"""
        response = self.client.get(reverse("booking_detail", args=[self.booking.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "bookings/booking_detail.html")
        self.assertContains(response, "Core Pilates")
        self.assertContains(response, "Pilates Studio")
        
        self.assertEqual(response.context["booking"], self.booking)

    @patch("bookings.views.send_booking_confirmation_email")
    def test_create_booking_view(self, mock_send_email):
        """Test creating a new booking"""
        new_schedule = ClassSchedule.objects.create(
            fitness_class=self.fitness_class,
            start_time=timezone.now() + timedelta(days=2),
            end_time=timezone.now() + timedelta(days=2, minutes=55),
            location="Pilates Studio",
            current_capacity=3,
        )
        
        self.assertEqual(Booking.objects.count(), 1)
        self.assertEqual(new_schedule.current_capacity, 3)
        
        response = self.client.post(reverse("create_booking", args=[new_schedule.id]))
        
        self.assertEqual(response.status_code, 302)
        
        self.assertEqual(Booking.objects.count(), 2)
        new_booking = Booking.objects.get(class_schedule=new_schedule)
        self.assertEqual(new_booking.user, self.user)
        self.assertEqual(new_booking.status, "confirmed")
        
        new_schedule.refresh_from_db()
        self.assertEqual(new_schedule.current_capacity, 4)
        
        mock_send_email.assert_called_once()

    def test_create_booking_for_past_class(self):
        """Test attempting to book a past class"""
        self.assertEqual(Booking.objects.count(), 1)
        
        response = self.client.post(reverse("create_booking", args=[self.past_schedule.id]))
        
        self.assertEqual(response.status_code, 302)
        
        self.assertEqual(Booking.objects.count(), 1)

    @patch("bookings.models.send_booking_cancellation_email")
    def test_cancel_booking_view(self, mock_send_email):
        """Test cancelling a booking"""
        self.assertEqual(self.booking.status, "confirmed")
        
        response = self.client.post(
            reverse("cancel_booking", args=[self.booking.id]),
            {"reason": "Cannot attend"},
        )
        
        self.assertEqual(response.status_code, 302)
        
        self.booking.refresh_from_db()
        self.assertEqual(self.booking.status, "cancelled")
        self.assertEqual(self.booking.cancellation_reason, "Cannot attend")
        
        mock_send_email.assert_called_once()