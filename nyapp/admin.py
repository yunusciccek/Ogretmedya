from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser  # Özel kullanıcı modelinizin adına göre değiştirin
from .models import Icerik



admin.site.register(CustomUser, UserAdmin)

@admin.register(Icerik)
class IcerikAdmin(admin.ModelAdmin):
    list_display = ('baslik', 'resim',)