from django.contrib import admin

# Register your models here.

from .models import Country, Total

class CountryAdmin(admin.ModelAdmin):
    class Meta:
	    model = Country

class TotalAdmin(admin.ModelAdmin):
    class Meta:
	    model = Total

admin.site.register(Country,CountryAdmin)
admin.site.register(Total,TotalAdmin)