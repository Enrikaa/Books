from django import forms
from django.contrib import admin
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _

from UsersApp.models import User


class CustomUserChangeForm(forms.ModelForm):
    """
    This custom User form is created to address a situation where using UserAdmin would lead to the import of User
    from django.contrib.auth.models. However, in this project, the User model needs to be imported from UsersApp.models.
    So, regular password validations are not inherited from the UserAdmin functionality due to this reason.
    """
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput, required=False)

    class Meta(UserChangeForm.Meta):
        model = User

    def clean_password(self):
        password = self.cleaned_data.get("password")
        if password:
            validate_password(password, user=self.instance)
        return password

    def save(self, commit=True):
        if self.cleaned_data.get("password"):
            self.instance.set_password(self.cleaned_data["password"])
        return super().save(commit)


@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    form = CustomUserChangeForm
    fieldsets = (
        (None, {"fields": ("password",)}),
        (_("Personal info"), {"fields": ("username", "email")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "user_permissions",
                )
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )
