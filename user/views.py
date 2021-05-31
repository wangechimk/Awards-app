from django.contrib.auth.decorators import login_required
from .models import Post,Profile
from django.shortcuts import render,redirect
from .forms import SignupForm,uploadForm
from django.contrib.auth import login, authenticate

# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('awards/landing')
    else:
        form = SignupForm()
    return render(request, 'user/signup.html', {'form': form })

def login(request):
    return render(request, 'user/login.html')

@login_required(login_url='/user/login/')
def profile(request):
    current_user = request.user.profile
    pics = Post.objects.filter(profile=current_user).all()
    return render(request, 'user/profile.html', {'pics':pics})

@login_required(login_url='/user/login/')
def upload(request):
    current_user = request.user.profile
    if request.method == 'POST':
        form = uploadForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.profile = current_user
            image.save()
        return redirect('awards/landing')
    else:
        form = uploadForm()
    return render(request, 'user/upload.html', {'form':form})


def search(request):
    if 'project' in request.GET and request.GET['project']:
        search_term = request.GET.get('project')
        res = Post.search_project(search_term)
        return render(request, 'user/search.html', {'res':res})
    else:
        return render(request, 'user/search.html')    