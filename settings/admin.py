from django.contrib import admin
from .models import ChurchSettings,ThemePreset

# Register your models here.
admin.site.register(ChurchSettings)
admin.site.register(ThemePreset)
