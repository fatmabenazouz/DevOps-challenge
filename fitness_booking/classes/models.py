from django.db import models

class Instructor(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField(blank=True, null=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    profile_image = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

class ClassCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name_plural = "Class Categories"
    
    def __str__(self):
        return self.name

class FitnessClass(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE, related_name='classes')
    category = models.ForeignKey(ClassCategory, on_delete=models.CASCADE, related_name='classes')
    duration_minutes = models.PositiveIntegerField()
    max_capacity = models.PositiveIntegerField()
    difficulty_level = models.CharField(
        max_length=20,
        choices=[
            ('beginner', 'Beginner'),
            ('intermediate', 'Intermediate'),
            ('advanced', 'Advanced'),
        ],
        default='intermediate'
    )
    equipment_required = models.TextField(blank=True, null=True)
    image = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Fitness Classes"
    
    def __str__(self):
        return self.title

class ClassSchedule(models.Model):
    fitness_class = models.ForeignKey(FitnessClass, on_delete=models.CASCADE, related_name='schedules')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    location = models.CharField(max_length=200)
    current_capacity = models.PositiveIntegerField(default=0)
    is_cancelled = models.BooleanField(default=False)
    cancellation_reason = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['start_time']
    
    def __str__(self):
        return f"{self.fitness_class.title} - {self.start_time.strftime('%Y-%m-%d %H:%M')}"
    
    @property
    def is_full(self):
        return self.current_capacity >= self.fitness_class.max_capacity
    
    @property
    def available_spots(self):
        return self.fitness_class.max_capacity - self.current_capacity