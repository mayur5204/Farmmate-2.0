from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import joblib
import os
from django.conf import settings


@login_required(login_url='login')
def croprecommendation(request):
    return render(request, 'crop_recommendation/croprecommendation.html')


def result(request):
    # Use the local model file instead of going outside the app directory
    model_path = os.path.join(settings.BASE_DIR, 'crop_recommendation', 'finalized_model.sav')
    
    # Fallback to the original location if local file doesn't exist
    if not os.path.exists(model_path):
        model_path = os.path.join(settings.BASE_DIR.parent, 'finalized_model.sav')
    
    cls = joblib.load(model_path)
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

    return render(request, 'crop_recommendation/result.html', {'ans': ans,'list_values':lis})
