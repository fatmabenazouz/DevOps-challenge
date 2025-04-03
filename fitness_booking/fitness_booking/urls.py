from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('classes/', include('classes.urls')),
    path('bookings/', include('bookings.urls')),
    path('', TemplateView.as_view(template_name='common/home.html'), name='home'),
]