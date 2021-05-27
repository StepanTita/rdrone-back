from django.contrib import admin

from authentication.models import CustomUser

admin.site.register(CustomUser)
