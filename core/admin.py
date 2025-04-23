from django.contrib import admin
from .models import Tepih, Zakazivanje, UserProfile

@admin.register(Zakazivanje)
class ZakazivanjeAdmin(admin.ModelAdmin):
    list_display = ['id', 'broj_tepiha', 'datum', 'status']

    def broj_tepiha(self, obj):
        return obj.tepisi.count()
    broj_tepiha.short_description = 'Broj tepiha'


admin.site.register(Tepih)
admin.site.register(UserProfile)
