from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from .models import Instructor, ClassCategory, FitnessClass, ClassSchedule


class InstructorModelTests(TestCase):
    def setUp(self):
        self.instructor = Instructor.objects.create(
            name="John Doe",
            email="john@example.com",
            bio="Experienced fitness instructor",
            phone_number="123-456-7890",
        )

    def test_instructor_creation(self):
        """Test that an instructor can be created properly"""
        self.assertEqual(Instructor.objects.count(), 1)
        self.assertEqual(self.instructor.name, "John Doe")
        self.assertEqual(self.instructor.email, "john@example.com")

    def test_instructor_str_representation(self):
        """Test the string representation of the Instructor model"""
        self.assertEqual(str(self.instructor), "John Doe")


class ClassCategoryModelTests(TestCase):
    def setUp(self):
        self.category = ClassCategory.objects.create(
            name="Yoga", description="Various yoga practices"
        )

    def test_category_creation(self):
        """Test that a class category can be created properly"""
        self.assertEqual(ClassCategory.objects.count(), 1)
        self.assertEqual(self.category.name, "Yoga")

    def test_category_str_representation(self):
        """Test the string representation of the ClassCategory model"""
        self.assertEqual(str(self.category), "Yoga")


class FitnessClassModelTests(TestCase):
    def setUp(self):
        self.instructor = Instructor.objects.create(
            name="Jane Smith", email="jane@example.com"
        )
        self.category = ClassCategory.objects.create(name="HIIT")
        self.fitness_class = FitnessClass.objects.create(
            title="Intense HIIT",
            description="High-intensity interval training",
            instructor=self.instructor,
            category=self.category,
            duration_minutes=45,
            max_capacity=20,
            difficulty_level="intermediate",
        )

    def test_fitness_class_creation(self):
        """Test that a fitness class can be created properly"""
        self.assertEqual(FitnessClass.objects.count(), 1)
        self.assertEqual(self.fitness_class.title, "Intense HIIT")
        self.assertEqual(self.fitness_class.instructor, self.instructor)
        self.assertEqual(self.fitness_class.category, self.category)

    def test_fitness_class_str_representation(self):
        """Test the string representation of the FitnessClass model"""
        self.assertEqual(str(self.fitness_class), "Intense HIIT")


class ClassScheduleModelTests(TestCase):
    def setUp(self):
        self.instructor = Instructor.objects.create(
            name="Jane Smith", email="jane@example.com"
        )
        self.category = ClassCategory.objects.create(name="HIIT")
        self.fitness_class = FitnessClass.objects.create(
            title="Intense HIIT",
            description="High-intensity interval training",
            instructor=self.instructor,
            category=self.category,
            duration_minutes=45,
            max_capacity=20,
            difficulty_level="intermediate",
        )
        
        self.start_time = timezone.now() + timedelta(days=1)
        self.end_time = self.start_time + timedelta(minutes=45)
        
        self.schedule = ClassSchedule.objects.create(
            fitness_class=self.fitness_class,
            start_time=self.start_time,
            end_time=self.end_time,
            location="Main Studio",
            current_capacity=5,
        )

    def test_schedule_creation(self):
        """Test that a class schedule can be created properly"""
        self.assertEqual(ClassSchedule.objects.count(), 1)
        self.assertEqual(self.schedule.fitness_class, self.fitness_class)
        self.assertEqual(self.schedule.location, "Main Studio")
        self.assertEqual(self.schedule.current_capacity, 5)

    def test_schedule_str_representation(self):
        """Test the string representation of the ClassSchedule model"""
        expected_str = f"{self.fitness_class.title} - {self.start_time.strftime('%Y-%m-%d %H:%M')}"
        self.assertEqual(str(self.schedule), expected_str)

    def test_is_full_property(self):
        """Test the is_full property of ClassSchedule"""
        self.assertFalse(self.schedule.is_full)
        
        self.schedule.current_capacity = self.fitness_class.max_capacity
        self.schedule.save()
        
        self.assertTrue(self.schedule.is_full)

    def test_available_spots_property(self):
        """Test the available_spots property of ClassSchedule"""
        self.assertEqual(self.schedule.available_spots, 15)
        
        self.schedule.current_capacity = 12
        self.schedule.save()
        
        self.assertEqual(self.schedule.available_spots, 8)


class ClassListViewTests(TestCase):
    def setUp(self):
        self.instructor = Instructor.objects.create(
            name="Jane Smith", email="jane@example.com"
        )
        self.category1 = ClassCategory.objects.create(name="Yoga")
        self.category2 = ClassCategory.objects.create(name="HIIT")
        
        self.class1 = FitnessClass.objects.create(
            title="Beginner Yoga",
            description="Introduction to yoga",
            instructor=self.instructor,
            category=self.category1,
            duration_minutes=60,
            max_capacity=15,
            difficulty_level="beginner",
        )
        
        self.class2 = FitnessClass.objects.create(
            title="Advanced HIIT",
            description="Intense workout",
            instructor=self.instructor,
            category=self.category2,
            duration_minutes=45,
            max_capacity=20,
            difficulty_level="advanced",
        )

    def test_class_list_view(self):
        """Test that the class list view displays all classes"""
        response = self.client.get(reverse("class_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "classes/class_list.html")
        self.assertContains(response, "Beginner Yoga")
        self.assertContains(response, "Advanced HIIT")
        
        self.assertEqual(len(response.context["classes"]), 2)
        self.assertEqual(len(response.context["categories"]), 2)

    def test_class_list_by_category(self):
        """Test filtering classes by category"""
        response = self.client.get(
            reverse("class_list_by_category", args=[self.category1.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Beginner Yoga")
        self.assertNotContains(response, "Advanced HIIT")
        
        self.assertEqual(len(response.context["classes"]), 1)
        self.assertEqual(response.context["category"], self.category1)