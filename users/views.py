from decouple import config
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import views as auth_views
from PIL import Image
from django.urls import reverse
from django.utils import timezone

from users.forms import UserCreationForms, ColourSettingsForm, UserCreationFromRequestForms, UserProfileForms, \
    SiteSettingsForm
from users.models import ColourSettings, SignUpRequest, SiteSettings, OsuOauthTemporaryCode, OsuOauthToken
from utility.osu_api.oauth import generate_authorize_url, get_access_token
from utility.osu_database import get_user_by_id, get_user_by_username, update_user_in_database
from utility.s3.utils import get_s3_client

S3_BUCKET_NAME = config('S3_BUCKET_NAME', default='')
S3_URL = config('S3_URL', default='')


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
    profile = request.user.profile
    site_settings = SiteSettings.objects.get(user=request.user)
    if request.method == 'POST':
        colour_form = ColourSettingsForm(request.POST, instance=colour_settings)
        profile_settings = UserProfileForms(request.POST, request.FILES, instance=profile)
        site_settings = SiteSettingsForm(request.POST, instance=request.user.sitesettings)
        if colour_form.is_valid() and profile_settings.is_valid() and site_settings.is_valid():
            colour_form.save()
            site_settings.save()
            if 'avatar' in request.FILES:
                osu_user = get_user_by_username(request.user.username)
                extension = request.FILES['avatar'].name.split('.')[-1]
                saved_settings = profile_settings.save(commit=False)
                saved_settings.name = f'{osu_user.user_id}.{extension}'
                saved_settings.save()
                # upload to s3
                s3_client = get_s3_client()
                s3_client.upload_fileobj(
                    # Get file from current profile instead since it's already resized
                    request.user.profile.avatar,
                    S3_BUCKET_NAME,
                    "avatar/" + saved_settings.name,
                    ExtraArgs={
                        'ACL': 'public-read',
                        'ContentType': request.FILES['avatar'].content_type
                    }
                )
                # Update S3 URL
                profile = request.user.profile
                profile.avatar_s3_url = f'{S3_URL}/avatar/{saved_settings.name}'
                profile.save()
                # Sync user info to osu! database
                osu_user.avatar = f'{osu_user.user_id}.{extension}'
                update_user_in_database(osu_user)
            messages.success(request, 'Settings saved successfully!')
            return redirect('settings')
    else:
        colour_form = ColourSettingsForm(instance=colour_settings)
        profile_settings = UserProfileForms(instance=profile)
        site_settings = SiteSettingsForm(instance=site_settings)
    return render(request, 'users/settings.html', {
        'colour_settings': colour_settings,
        'colour_form': colour_form,
        'profile_settings': profile_settings,
        'site_settings': site_settings,
        'osu_oauth_url': generate_authorize_url(redirect_uri=request.build_absolute_uri(reverse("osu_oauth_redirect"))),
        'oauth_token': OsuOauthToken.objects.filter(user=request.user).first() if OsuOauthToken.objects.filter(user=request.user).count() > 0 else None
    })


@login_required
def osu_oauth_redirect(request):
    code = request.GET.get('code')
    if code is None:
        return redirect('settings')
    else:
        temp_code = OsuOauthTemporaryCode.objects.filter(user=request.user)
        if temp_code.count() > 0:
            temp_code = temp_code.first()
            temp_code.code = code
            temp_code.save()
        else:
            OsuOauthTemporaryCode.objects.create(
                user=request.user,
                code=code
            )
        token = get_access_token(code=code)
        if token is None:
            return redirect('settings')
        else:
            temp_token = OsuOauthToken.objects.filter(user=request.user)
            if temp_token.count() > 0:
                temp_token = temp_token.first()
                temp_token.access_token = token['access_token']
                temp_token.refresh_token = token['refresh_token']
                temp_token.expires_in = token['expires_in']
                temp_token.token_type = token['token_type']
                temp_token.time_created = timezone.now()
                temp_token.save()
            else:
                OsuOauthToken.objects.create(
                    user=request.user,
                    access_token=token['access_token'],
                    refresh_token=token['refresh_token'],
                    expires_in=token['expires_in'],
                    token_type=token['token_type']
                )
            return redirect('settings')
