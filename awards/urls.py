from django.urls import path, include
from . import views
import awards
app_name='awards'
urlpatterns = [
    path('landing/', views.landing, name='landing'),
] 