from django.urls import path
from .views import mainSite

urlpatterns = [
    path('', mainSite)
]