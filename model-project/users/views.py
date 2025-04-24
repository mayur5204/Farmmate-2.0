from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import logout as auth_logout
from .forms import UserRegisterForm

def login(request):
    """View function for user login"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request, f'Welcome, {username}!')
            return redirect('homepage')
        else:
            messages.warning(request, 'Invalid username or password')
    return render(request, 'users/login.html')

def register(request):
    """View function for user registration"""
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created successfully for {username}! You can now log in.')
            return redirect('login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

def logout(request):
    """View function for user logout"""
    auth_logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('homepage')
