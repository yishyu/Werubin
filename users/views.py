from django.shortcuts import render
from django.urls import reverse
from users.forms import RegistrationForm, ResetPasswordForm
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login as Login
from django.contrib import messages
from users.models import User, PasswordForgottenRequest
from django.core.mail import send_mail
import datetime as dt
from django.conf import settings
from django.contrib.auth.decorators import login_required


# Sign Up View
def registration(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(form.cleaned_data['password1'])
            user.email = form.cleaned_data['email']
            user.save()
            authuser = authenticate(username=user.username, password=form.cleaned_data['password1'])
            if authuser:
                Login(request, authuser)
            return HttpResponseRedirect(reverse("feeds:front_feed"))
        else:
            return render(request, 'registration/registration.html', locals())

    form = RegistrationForm()
    return render(request, 'registration/registration.html', locals())


def forgotpass(request):
    if request.method == "POST":
        email = request.POST["email"].lower().strip()
        user_qs = User.objects.filter(email=email)
        validity = dt.datetime.now() + dt.timedelta(hours=24)
        if user_qs.count() > 0:
            passforgot_obj = PasswordForgottenRequest.objects.create(user=user_qs.first(), validity_end=validity)
            if not settings.DEBUG:
                send_mail(
                    'Werubin Password Recovery',
                    f"Dear User, we received your request for a password reinitialisation. Please click on this link to reset your password: https://{request.META['HTTP_HOST']}/users/reset-password/{passforgot_obj.link}",
                    settings.EMAIL_HOST_USER,
                    [email],
                    fail_silently=False,
                )
            messages.add_message(
                request, messages.SUCCESS, f"An email has been sent to {email}"
            )
            return HttpResponseRedirect(reverse("users:login"))
        else:
            messages.add_message(
                request, messages.ERROR, f"The email you entered ({email}) doesn't match any user in our database."
            )
    return render(request, 'registration/forgotpass.html', locals())


def resetpass(request, key):
    passforgot_obj = PasswordForgottenRequest.objects.get(link=key)  # 404 if not found
    user = passforgot_obj.user
    if request.method == "POST":
        form = ResetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(
                request, messages.SUCCESS, "Your password has been reset !"
            )
            return HttpResponseRedirect(reverse("users:login"))
        else:
            return render(request, 'registration/resetpass.html', locals())

    form = ResetPasswordForm(user)
    return render(request, 'registration/resetpass.html', locals())


@login_required
def profile(request):
    return render(request, 'self_profile.html', locals())
