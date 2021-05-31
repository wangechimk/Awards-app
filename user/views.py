from django.contrib.auth.decorators import login_required
from .models import Post,Profile,Rating
from django.shortcuts import render,redirect
from .forms import SignupForm,uploadForm,rateProject
from django.contrib.auth import login, authenticate
from django.http import HttpResponseRedirect
import random

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



def project(request, post):
    post = Post.objects.get(title=post)
    ratings = Rating.objects.filter(user=request.user, post=post).first()
    rating_status = None
    if ratings is None:
        rating_status = False
    else:
        rating_status = True
    if request.method == 'POST':
        form = rateProject(request.POST)
        if form.is_valid():
            rate = form.save(commit=False)
            rate.user = request.user
            rate.post = post
            rate.save()
            post_ratings = Rating.objects.filter(post=post)

            design_ratings = [d.design for d in post_ratings]
            design_average = sum(design_ratings) / len(design_ratings)

            usability_ratings = [us.usability for us in post_ratings]
            usability_average = sum(usability_ratings) / len(usability_ratings)

            content_ratings = [content.content for content in post_ratings]
            content_average = sum(content_ratings) / len(content_ratings)

            score = (design_average + usability_average + content_average) / 3
            print(score)
            rate.design_average = round(design_average, 2)
            rate.usability_average = round(usability_average, 2)
            rate.content_average = round(content_average, 2)
            rate.score = round(score, 2)
            rate.save()
            return HttpResponseRedirect(request.path_info)
    else:
        form = rateProject()
    params = {
        'post': post,
        'rating_form': form,
        'rating_status': rating_status

    }
    return render(request, 'rate.html', {'post':project, 'form':form})
