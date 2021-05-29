from django.shortcuts import render,redirect
from .forms import SignupForm
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
            return redirect('landing')
    else:
        form = SignupForm()
    return render(request, 'user/signup.html', {'form': form })

def login(request):
    return render(request, 'user/login.html')