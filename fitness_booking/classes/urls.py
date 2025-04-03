from django.urls import path
from . import views

urlpatterns = [
    path('', views.class_list, name='class_list'),
    path('category/<int:category_id>/', views.class_list_by_category, name='class_list_by_category'),
    path('<int:class_id>/', views.class_detail, name='class_detail'),
    path('schedule/<int:schedule_id>/', views.schedule_detail, name='schedule_detail'),
    path('instructor/<int:instructor_id>/', views.instructor_detail, name='instructor_detail'),
]