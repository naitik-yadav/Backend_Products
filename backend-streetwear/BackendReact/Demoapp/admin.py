from django.contrib import admin

from .models import Nike


class NikeAdmin(admin.ModelAdmin):
    list_display = ("ShoeName", "ShoeNumber", "ShoeType", "Gender", "Price", "images")

admin.site.register(Nike, NikeAdmin)
