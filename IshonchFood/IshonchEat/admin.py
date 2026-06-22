from django.contrib import admin

# Register your models here.
from .models import Restaurant, Category, MenuItem

admin.site.register(Restaurant)
admin.site.register(Category)
admin.site.register(MenuItem)
