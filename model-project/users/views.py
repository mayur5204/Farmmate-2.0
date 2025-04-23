from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.utils import timezone
import time  # Import time module for cache busting
import base64
import json
from django.core.files.base import ContentFile
from .forms import UserUpdateForm, ProfileUpdateForm, ProfilePictureForm, CustomPasswordChangeForm
from .models import UserProfile
from community.models import Post, Comment  # Import community models

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
    # Initialize form_type to track which form was submitted
    form_type = request.POST.get('form_type', None)
    
    if request.method == 'POST' and form_type == 'profile_info':
        # Handle regular profile info update
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, instance=request.user.profile)
        profile_picture_form = ProfilePictureForm(instance=request.user.profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile information has been updated!')
            return redirect('profile')
            
    elif request.method == 'POST' and form_type == 'profile_picture':
        # Handle profile picture update separately
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
        
        # Check if we have a cropped image from JavaScript
        if 'cropped_image' in request.POST:
            # Process the cropped image data
            cropped_data = request.POST.get('cropped_image')
            if cropped_data:
                # Remove the "data:image/png;base64," part
                format, imgstr = cropped_data.split(';base64,')
                ext = format.split('/')[-1]
                
                # Create ContentFile from decoded base64 data
                data = ContentFile(base64.b64decode(imgstr), name=f'profile_pic_{request.user.username}.{ext}')
                
                # Save the new image
                request.user.profile.profile_picture = data
                request.user.profile.save()
                
                messages.success(request, 'Your profile picture has been updated!')
                return redirect(f'profile?t={int(time.time())}')
        else:
            # Use the regular form approach if no cropped image
            profile_picture_form = ProfilePictureForm(request.POST, request.FILES, instance=request.user.profile)
            
            if profile_picture_form.is_valid():
                profile_picture_form.save()
                messages.success(request, 'Your profile picture has been updated!')
                return redirect(f'profile?t={int(time.time())}')
    else:
        # GET request - display forms
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
        profile_picture_form = ProfilePictureForm(instance=request.user.profile)
    
    # Add timestamp to profile picture URL to prevent browser caching
    profile_pic_url = f"{request.user.profile.profile_picture.url}?t={int(time.time())}"
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'profile_picture_form': profile_picture_form,
        'active_tab': 'profile',
        'profile_pic_url': profile_pic_url
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
    # Fetch the most recent community posts
    recent_posts = Post.objects.select_related('author').prefetch_related('comments')[:2]
    
    # Add timestamp to profile picture URL to prevent browser caching
    profile_pic_url = f"{request.user.profile.profile_picture.url}?t={int(time.time())}"
    
    context = {
        'active_tab': 'dashboard',
        'date_today': timezone.now(),
        'recent_posts': recent_posts,
        'profile_pic_url': profile_pic_url
    }
    return render(request, 'users/dashboard.html', context)

class CustomPasswordChangeView(PasswordChangeView):
    form_class = CustomPasswordChangeForm
    success_url = reverse_lazy('settings')
    template_name = 'users/password_change.html'
    
    def form_valid(self, form):
        messages.success(self.request, 'Your password has been updated!')
        return super().form_valid(form)
