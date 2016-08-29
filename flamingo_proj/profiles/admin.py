from django.contrib import admin

from .models import MyUser, Profile
# Register your models here.


class MyUserAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password', 'date_joined')}),
        ('User Information', {'fields': (('first_name', 'last_name'),)}),
    )


class ProfileAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('user', )}),
        ('Profile Information', {'fields': ('birthdate', 'rating', 'follows')}),
    )
    filter_horizontal = ('follows',)


admin.site.register(MyUser, MyUserAdmin)
admin.site.register(Profile, ProfileAdmin)
