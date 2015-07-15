from django.contrib import admin
from .models import Category, Bicycle, UserProfile

class CategoryAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug': ('name',)}

admin.site.register(Category, CategoryAdmin)
admin.site.register(Bicycle)
admin.site.register(UserProfile)
