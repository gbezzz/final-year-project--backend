from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm


# Register your models here.
class CustomUserAdmin(UserAdmin):
    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = [
        "username",
        "email",
        "full_name",
        "is_staff",
        # "gender",
        "role",
        "phone_number",
    ]
    fieldsets = UserAdmin.fieldsets + (
        (None, {"fields": ("gender", "role", "phone_number")}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {"fields": ("gender", "role", "phone_number")}),
    )


admin.site.register(CustomUser, CustomUserAdmin)
