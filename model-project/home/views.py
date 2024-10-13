from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout


import joblib


# Create your views here.


def home(request):
    return render(request, 'index.html')

def register(request):
    return render(request, 'register.html')

@login_required(login_url='login')

def croprecommendation(request):

    return render(request, 'croprecommendation.html')

def products(request):
    return render(request, 'products.html')

def aboutUs(request):
    return render(request, 'aboutUs.html')

def resources(request):
    return render(request, 'resources.html')

def help(request):
    return render(request, 'help.html')

def login(request):

    if request.method == 'POST':
        # Determine if the form is for login or signup
        if 'login' in request.POST:  # Check if it's a login form
            username = request.POST.get('username')
            password = request.POST.get('password')
            
            # Authenticate the user
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)  # Corrected to use auth_login
                messages.success(request, 'Login successful!')  # Add success message
                return redirect('homepage')  # Redirect to dashboard after login
            else:
                messages.error(request, 'Invalid username or password')
        
        elif 'signup' in request.POST:  # Check if it's a signup form
            username = request.POST.get('username')
            password = request.POST.get('password')
            email = request.POST.get('email')
            confirmpassword = request.POST.get('confirmpassword')
            
            # Check if the username already exists
            if User.objects.filter(username=username).exists():
                messages.warning(request, 'Username already taken')
            elif(password != confirmpassword):
                messages.warning(request, 'Password and Confirm Password do not match')
            else:
                # Create a new user
                user = User.objects.create_user(username=username, password=password, email=email)
                user.save()
                messages.success(request, 'Account created successfully. Please log in.')  # Success message
                return redirect('login')  # Redirect to login page after signup

    

    return render(request, 'login.html')

def logout(request):
    auth_logout(request)
    messages.success(request, 'You have been logged out successfully.')  # Success message on logout
    return redirect('homepage') 

def weather(request):
    return render(request, 'weatherForecast.html')


def result(request):
    cls = joblib.load('../finalized_model.sav')
    lis = []

    if request.method == 'POST':
        lis.append(request.POST.get('nitrogen'))
        lis.append(request.POST.get('phosphorus'))
        lis.append(request.POST.get('potassium'))
        lis.append(request.POST.get('temperature'))
        lis.append(request.POST.get('humidity'))
        lis.append(request.POST.get('ph'))
        lis.append(request.POST.get('rainfall'))
    else:
        lis.append(request.GET.get('nitrogen'))
        lis.append(request.GET.get('phosphorus'))
        lis.append(request.GET.get('potassium'))
        lis.append(request.GET.get('temperature'))
        lis.append(request.GET.get('humidity'))
        lis.append(request.GET.get('ph'))
        lis.append(request.GET.get('rainfall'))
    
  
    ans = cls.predict([lis])
 



    return render(request, 'result.html', {'ans': ans,'list_values':lis})