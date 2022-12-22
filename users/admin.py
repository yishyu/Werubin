from django.contrib import admin
from users.models import User, PasswordForgottenRequest


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id", "username", "first_name", "last_name", "gender",
    )
    list_filter = ("gender", "username")
    search_fields = ("first_name", "last_name", "email", "username")


@admin.register(PasswordForgottenRequest)
class PasswordForgottenRequestAdmin(admin.ModelAdmin):
    list_display = (
        'link', 'validity_end'
    )
