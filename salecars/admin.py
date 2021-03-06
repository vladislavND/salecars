from django.contrib import admin
from salecars.models import *


@admin.register(Users)
class UserAdmin(admin.ModelAdmin):
    list_fields = ('__all__')


@admin.register(Auto)
class AutoAdmin(admin.ModelAdmin):
    list_fields = ('__all__')
    list_display = ['model', 'price', 'year', 'date']


@admin.register(Models)
class ModelsAdmin(admin.ModelAdmin):
    list_fields = ('__all__')
    list_display = ['name']


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_fields = ('__all__')
    list_display = ['name']


@admin.register(Marks)
class MarksAdmin(admin.ModelAdmin):
    list_fields = ('__all__')
    list_display = ['name']


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_fields = ('__all__')
    list_display = ['name']


@admin.register(Adsense)
class AdsenseAdmin(admin.ModelAdmin):
    list_fields = ('__all__')
    list_display = ['auto', 'user']


@admin.register(UserAutoFilter)
class UserAutoFilterAdmin(admin.ModelAdmin):
    list_fields = ('__all__')
    list_display = ['model', 'price_to', 'price_from']




