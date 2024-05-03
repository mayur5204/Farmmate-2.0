from django.shortcuts import render, redirect


import joblib




def home(request):
    return render(request, 'index.html')

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
    return render(request, 'login.html')

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