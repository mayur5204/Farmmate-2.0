from django.shortcuts import render

# Core views for main pages
def home(request):
    return render(request, 'index.html')

def aboutUs(request):
    return render(request, 'aboutUs.html')

def resources(request):
    return render(request, 'resources.html')

def help(request):
    return render(request, 'help.html')
