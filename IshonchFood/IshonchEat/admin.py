from django.contrib import admin

# Register your models here.
from .models import Advertisement,Category,Restaurant,CategoryMenu, MenuItem

admin.site.register(Advertisement)
admin.site.register(Category)
admin.site.register(Restaurant)
admin.site.register(CategoryMenu)
admin.site.register(MenuItem)

