from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from users.models import ColourSettings


def homepage(request):
    if request.user.is_authenticated:
        return render(request, 'homepage.html', {'colour_settings': ColourSettings.objects.get(user=request.user)})
    else:
        return render(request, 'homepage.html')
