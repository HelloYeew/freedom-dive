from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(ColourSettings)
admin.site.register(SignUpRequest)
admin.site.register(Profile)
admin.site.register(SiteSettings)
admin.site.register(OsuOauthTemporaryCode)
admin.site.register(OsuOauthToken)