from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User1
# Register your models here.
class UserAd(admin.ModelAdmin):
    class Meta:
        abstract = True


admin.site.register(User1, UserAd)

