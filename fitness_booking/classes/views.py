from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import FitnessClass, ClassCategory, ClassSchedule, Instructor

def class_list(request):
    categories = ClassCategory.objects.all()
    classes = FitnessClass.objects.all()
    
    category_id = request.GET.get('category')
    if category_id:
        classes = classes.filter(category_id=category_id)
    
    upcoming_schedules = ClassSchedule.objects.filter(
        start_time__gt=timezone.now(),
        is_cancelled=False
    ).order_by('start_time')[:10]
    
    context = {
        'categories': categories,
        'classes': classes,
        'upcoming_schedules': upcoming_schedules
    }
    
    return render(request, 'classes/class_list.html', context)

def class_list_by_category(request, category_id):
    category = get_object_or_404(ClassCategory, id=category_id)
    classes = FitnessClass.objects.filter(category=category)
    
    context = {
        'category': category,
        'classes': classes
    }
    
    return render(request, 'classes/class_list_by_category.html', context)

def class_detail(request, class_id):
    fitness_class = get_object_or_404(FitnessClass, id=class_id)
    
    upcoming_schedules = ClassSchedule.objects.filter(
        fitness_class=fitness_class,
        start_time__gt=timezone.now(),
        is_cancelled=False
    ).order_by('start_time')
    
    context = {
        'fitness_class': fitness_class,
        'upcoming_schedules': upcoming_schedules
    }
    
    return render(request, 'classes/class_detail.html', context)

def schedule_detail(request, schedule_id):
    schedule = get_object_or_404(ClassSchedule, id=schedule_id)
    
    context = {
        'schedule': schedule
    }
    
    return render(request, 'classes/schedule_detail.html', context)

def instructor_detail(request, instructor_id):
    instructor = get_object_or_404(Instructor, id=instructor_id)
    
    upcoming_schedules = ClassSchedule.objects.filter(
        fitness_class__instructor=instructor,
        start_time__gt=timezone.now(),
        is_cancelled=False
    ).order_by('start_time')
    
    context = {
        'instructor': instructor,
        'upcoming_schedules': upcoming_schedules
    }
    
    return render(request, 'classes/instructor_detail.html', context)