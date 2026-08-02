from django.contrib import admin
from django.urls import path
from api.views import vista

urlpatterns = [
    path('admin/', admin.site.urls),
    path('vista/', vista),
]