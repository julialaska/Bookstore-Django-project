from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('bookstoreapp.urls')),
    path('admin/', admin.site.urls),
]
