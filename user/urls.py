from django.urls import path, include
from . import views
import user
app_name='user'
urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('profile/', views.profile, name='profile'),
    path('upload/', views.profile, name='upload'),
    path('search/', views.search, name='search'),
] 