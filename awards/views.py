from django.shortcuts import render
from user.models import Post

# Create your views here.
def landing(request):
    posts=Post.objects.all().order_by('-created_on')
    return render(request, 'awards/landing.html', {'posts': posts})