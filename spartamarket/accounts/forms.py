from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth import get_user_model
from django.urls import reverse


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.fields.get("password"):
            password_help_text = (
                "You can change the password " '<a href="{}">here</a>.'
            ).format(f"{reverse('accounts:change_password')}")
            self.fields["password"].help_text = password_help_text

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = UserCreationForm.Meta.fields