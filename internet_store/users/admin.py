from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Users

# Register your models here.
class CustomUserAdmin(UserAdmin):
    list_display=('first_name', 'last_name', 'password', 'email')
    list_display_links = ('email', 'first_name', 'last_name')
    readonly_fields = ('last_login', 'date_joined')
    ordering = ['-date_joined']
    list_per_page = 20
    list_max_show_all = 100

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(Users, CustomUserAdmin)