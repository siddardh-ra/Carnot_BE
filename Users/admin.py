from django.contrib import admin
from .models import UserProfile
from .models import PasswordReset

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(PasswordReset)
