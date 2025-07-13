from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('tracker.urls')),  # ✅ important line!
    path('admin/', admin.site.urls),
]
