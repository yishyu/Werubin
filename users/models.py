from django.db import models
from django.contrib.auth.models import AbstractUser
import hashlib


class User(AbstractUser):
    gender_choices = (
        ("M", "Male"),
        ("F", "Female"),
        ("O", 'Other')
    )
    gender = models.CharField("Gender", max_length=10, choices=gender_choices)
    birthdate = models.DateField('Birthdate', auto_now=False, auto_now_add=False, null=True, blank=True)
    profile_picture = models.ImageField("Profile Picture", upload_to='profile/images', height_field=None, width_field=None, max_length=None, blank=True, null=True)
    followers = models.ManyToManyField("self", verbose_name="Followers", blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class PasswordForgottenRequest(models.Model):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    validity_end = models.DateTimeField("validity", auto_now=False, auto_now_add=False)
    link = models.CharField("link", max_length=300)

    def save(self, *args, **kwargs):
        self.link = hashlib.sha256((self.user.email + str(self.validity_end)).encode("utf-8")).hexdigest()
        super().save(*args, **kwargs)
