from django.contrib import admin
from .models import Instructor, ClassCategory, FitnessClass, ClassSchedule

@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone_number']
    search_fields = ['name', 'email']

@admin.register(ClassCategory)
class ClassCategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(FitnessClass)
class FitnessClassAdmin(admin.ModelAdmin):
    list_display = ['title', 'instructor', 'category', 'duration_minutes', 'max_capacity', 'difficulty_level']
    list_filter = ['category', 'difficulty_level', 'instructor']
    search_fields = ['title', 'description', 'instructor__name']

@admin.register(ClassSchedule)
class ClassScheduleAdmin(admin.ModelAdmin):
    list_display = ['fitness_class', 'start_time', 'end_time', 'location', 'current_capacity', 'is_cancelled']
    list_filter = ['is_cancelled', 'fitness_class__category', 'start_time']
    search_fields = ['fitness_class__title', 'location']
    date_hierarchy = 'start_time'