from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('', include('accounts.urls')),
    path('students/', include('students.urls')),
    path('professors/', include('professors.urls')),
    path('courses/', include('courses.urls')),
    path('library/', include('library.urls')),
    path('research/', include('research.urls')),
    path('societies/', include('societies.urls')),
    path('tuition/', include('tuition.urls')),
    path('alumni/', include('alumni.urls')),
]