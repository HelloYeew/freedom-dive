"""ayaka URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import path, include

from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView

from users import views as users_views

urlpatterns = [
    path(
        "favicon.ico",
        RedirectView.as_view(url=staticfiles_storage.url("favicon.ico")),
    ),
    path('admin/', admin.site.urls),
    path('mdeditor/', include('mdeditor.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    # Disable signup since we allow only to register via client
    # path('signup/', users_views.signup, name='signup'),
    path('signup/', users_views.sign_up_from_request, name='sign_up_from_request'),
    path('logout/', users_views.LogoutAndRedirect.as_view(), name='logout'),
    path('settings/', users_views.settings, name='settings'),
    path('osu-oauth/token', users_views.osu_oauth_token, name='osu_oauth_token'),
    path('osu-oauth/redirect', users_views.osu_oauth_redirect, name='osu_oauth_redirect'),
    path('api/', include('client_api.urls')),
    path('', include('apps.urls')),
    path('', include('utility.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)