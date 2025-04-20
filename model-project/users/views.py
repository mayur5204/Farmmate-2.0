from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from .forms import UserUpdateForm, ProfileUpdateForm, CustomPasswordChangeForm
from .models import UserProfile

def login(request):
    if request.method == 'POST':
        # Only handle login requests in this view
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('homepage')
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'users/login.html')

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        confirmpassword = request.POST.get('confirmpassword')
        
        # Check if the username already exists
        if User.objects.filter(username=username).exists():
            messages.warning(request, 'Username already taken')
            return render(request, 'users/register.html')
        elif(password != confirmpassword):
            messages.warning(request, 'Password and Confirm Password do not match')
            return render(request, 'users/register.html')
        else:
            # Create a new user
            user = User.objects.create_user(username=username, password=password, email=email)
            user.save()
            messages.success(request, 'Account created successfully. Please log in.')
            return redirect('login')
            
    return render(request, 'users/register.html')

def logout(request):
    auth_logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('homepage')

@login_required
def profile(request):
    """View function for user profile"""
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'active_tab': 'profile'
    }
    return render(request, 'users/profile.html', context)

@login_required
def settings(request):
    """View function for user settings"""
    context = {
        'active_tab': 'settings'
    }
    return render(request, 'users/settings.html', context)

@login_required
def dashboard(request):
    """View function for user dashboard"""
    context = {
        'active_tab': 'dashboard'
    }
    return render(request, 'users/dashboard.html', context)

class CustomPasswordChangeView(PasswordChangeView):
    form_class = CustomPasswordChangeForm
    success_url = reverse_lazy('settings')
    template_name = 'users/password_change.html'
    
    def form_valid(self, form):
        messages.success(self.request, 'Your password has been updated!')
        return super().form_valid(form)
