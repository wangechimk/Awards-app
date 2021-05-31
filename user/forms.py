from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Post,Rating



class SignupForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
  
class Meta:
    model = User
    exclude = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )
    
    
class uploadForm(forms.ModelForm):
  class Meta:
    model = Post
    exclude = ['profile', 'created_on']

class rateProject(forms.ModelForm):
  class Meta:
        model = Rating
        fields = ['design', 'usability', 'content']