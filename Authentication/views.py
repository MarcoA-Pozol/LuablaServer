from django.shortcuts import render, redirect, HttpResponse
from . forms import UserRegisterForm, LoginForm
from django.contrib import auth, messages

def authentication_home(request):
    return HttpResponse("Welcome to Authentication")

def register(request):
    if request.method=="POST":
        form = UserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                #Create new User
                user = form.save(commit=False)
                user.save()

                auth.login(request, user)
                return redirect('languages-selection')
            except Exception as e:
                form.add_error(None, f"Error during User creation: {e}")
                print(f"Error during User creation: {e}")
    else:
        form = UserRegisterForm()
    context = {'form':form}
    return render(request, "register.html", context)

def login(request):
    if request.user.is_authenticated:
        return redirect('languages-selection')
    
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = auth.authenticate(request, username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect('languages-selection')
            else:
                messages.error(request, 'Invalid username or password')
    else:
        form = LoginForm()
    
    context = {'form': form}
    return render(request, 'login.html', context)

def logout(request):
    auth.logout(request)
    return redirect('welcome')





"""def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = auth.authenticate(request, username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect('languages')
            else:
                messages.error(request, 'Invalid username or password')
    else:
        form = LoginForm()
    
    context = {'form': form}
    return render(request, 'login.html', context)
"""