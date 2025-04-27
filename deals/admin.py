from django.contrib import admin
from .models import User, Category, Deal

# admin.site.register(User)
# admin.site.register(Category)
# admin.site.register(Deal)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username','email','role','is_active','is_staff')
    list_filter = ('role', 'is_active', 'is_staff')
    search_fields = ('username', 'email')

@admin.register(Category)
class categoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Deal)
class DealAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'owner', 'created_at', 'expiration_date', 'is_approved')
    list_filter = ('category','description','owner__username')
    