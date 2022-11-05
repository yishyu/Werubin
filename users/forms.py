from django.contrib.auth.forms import UserCreationForm
from users.models import User


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
            # 'profile_picture',
            'email',
            'password1',
            'password2'
        ]

    def clean(self, admin=False):
        cleaned_data = super().clean()
        if admin:
            return
        email = cleaned_data.get("email").lower()

        if User.objects.filter(email=email).count() > 0:
            msg = "this email is already in use"
            self.add_error('email', msg)
