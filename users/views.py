from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import views as auth_views

from users.forms import UserCreationForms, UserSettingsForm, UserCreationFromRequestForms
from users.models import ColourSettings, SignUpRequest
from utility.osu_database import get_user_by_id


class LogoutAndRedirect(auth_views.LogoutView):
    # Redirect to / after logout
    def get_next_page(self):
        return '/'


def signup(request):
    if request.method == 'POST':
        form = UserCreationForms(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created successfully for {username}! Now you can login.')
            return redirect('login')
    else:
        form = UserCreationForms()
    return render(request, 'users/signup.html', {'form': form})

def sign_up_from_request(request):
    # get request id and authentication key from querystring
    # example URL : /signup/?id=1&auth_key=1234567890
    request_id = request.GET.get('id')
    auth_key = request.GET.get('auth_key')
    if request_id is None or auth_key is None:
        return render(request, '404.html', status=404)
    sign_up_request = SignUpRequest.objects.filter(id=request_id)
    if sign_up_request.count() == 0:
        messages.error(request, 'Request invalid')
        return redirect('homepage')
    else:
        sign_up_request = sign_up_request.first()
    if sign_up_request.done:
        messages.error(request, 'Request already done')
        return redirect('homepage')
    osu_user_info = get_user_by_id(sign_up_request.osu_user_id)
    if sign_up_request.authentication_key == auth_key:
        form = UserCreationFromRequestForms()
        if request.method == 'POST':
            form = UserCreationFromRequestForms(request.POST)
            if form.is_valid():
                username = sign_up_request.username
                User.objects.create(
                    username=username,
                    email=osu_user_info.email,
                    password=make_password(form.cleaned_data.get('password1'))
                )
                messages.success(request, f'Account created successfully for {username}! Now you can login.')
                sign_up_request.done = True
                sign_up_request.save()
                return redirect('login')
            else:
                messages.error(request, 'Invalid form, please try again')
                return redirect('homepage')
        else:
            return render(request, 'users/signup_from_request.html', {
                'form': form,
                'username': sign_up_request.username
            })
    else:
        messages.error(request, 'Request invalid')
        return redirect('homepage')

@login_required
def settings(request):
    colour_settings = ColourSettings.objects.filter(user=request.user).first()
    if request.method == 'POST':
        form = UserSettingsForm(request.POST, instance=colour_settings)
        if form.is_valid():
            form.save()
            messages.success(request, 'Settings saved successfully!')
            return redirect('settings')
    else:
        form = UserSettingsForm(instance=colour_settings)
    return render(request, 'users/settings.html', {
        'colour_settings': colour_settings,
        'form': form
    })
