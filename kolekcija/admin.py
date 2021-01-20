from django.contrib import admin
from . models import film
from .models import izvodac, pjesma, album

# Register your models here.

admin.site.register(izvodac)
admin.site.register(pjesma)
admin.site.register(album)