from django.contrib import admin
from django.urls import path, include
from . import views
#static files and media files configuration
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('Patients/', include('patients.urls')),
    path('Doctors/', include('doctors.urls')),
    path('Appointments/', include('appointments.urls')),
    path('Rating/', include('rating.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)