from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import TaskModel, CalendarTaskModel, UserModel


class CustomUserAdmin(UserAdmin):
    pass


class CustomTaskAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'title',
        'status'
    ]


admin.site.register(TaskModel, CustomTaskAdmin)
admin.site.register(CalendarTaskModel, CustomTaskAdmin)
admin.site.register(UserModel, CustomUserAdmin)
