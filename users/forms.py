from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from users.models import User
from django.contrib.auth import get_user_model


# Sign Up Form
class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'birthdate',
            'gender',
            'email',
            'password1',
            'password2'
        ]

    def clean(self, admin=False):
        cleaned_data = super().clean()
        if admin:
            return
        try:
            email = cleaned_data.get("email").lower()
            if User.objects.filter(email=email).count() > 0:
                msg = "This email is already in use"
                self.add_error('email', msg)
        except AttributeError:
            # missing attribute means cleaned data returned an error
            pass


class ResetPasswordForm(SetPasswordForm):
    class Meta:
        model = get_user_model()
        fields = ['new_password1', 'new_password2']
