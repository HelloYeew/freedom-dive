from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from users.models import ColourSettings


# Create your views here.

@login_required
def homepage(request):
    colour_settings = ColourSettings.objects.filter(user=request.user).first()
    return render(request, 'homepage.html', {
        'colour_settings': colour_settings
    })
