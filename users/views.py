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
from django.shortcuts import get_object_or_404
from users.decorators import no_user
from django.contrib.auth import logout as django_logout
from travels.models import Tag
import os


# Sign Up View
@no_user
def registration(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(form.cleaned_data['password1'])
            user.email = form.cleaned_data['email'].lower()
            user.save()
            authuser = authenticate(username=user.username, password=form.cleaned_data['password1'])
            if authuser:
                Login(request, authuser)
            return HttpResponseRedirect(reverse("feeds:front_feed"))
        else:
            return render(request, 'registration/registration.html', locals())
    else:
        form = RegistrationForm()
    return render(request, 'registration/registration.html', locals())


@no_user
def forgotpass(request):
    if request.method == "POST":
        email = request.POST["email"].lower().strip()
        user_qs = User.objects.filter(email=email)
        validity = dt.datetime.now() + dt.timedelta(hours=24)
        if user_qs.count() > 0:
            passforgot_obj = PasswordForgottenRequest.objects.create(user=user_qs.first(), validity_end=validity)
            #if not settings.DEBUG:
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
    return render(request, 'registration/forgotPass.html', locals())


@no_user
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
            return render(request, 'registration/resetPass.html', locals())

    form = ResetPasswordForm(user)
    return render(request, 'registration/resetPass.html', locals())


@login_required
def profile(request, username):
    user = get_object_or_404(User, username=username)
    print(user.birthdate)
    if request.method == "POST":
        data = request.POST
        if request.user.id == user.id:
            first_name = data['first_name']
            last_name = data['last_name']
            birthdate = data['birthdate']
            birthdate_year = birthdate.split("-")[0]
            birthdate_month = birthdate.split("-")[1]
            birthdate_day = birthdate.split("-")[2]
            birthdate_save = dt.date(int(birthdate_year), int(birthdate_month), int(birthdate_day))

            print("the data ", data)
            user.first_name = first_name
            user.last_name = last_name
            user.birthdate = birthdate_save
            user.gender = data['gender']
            user.profile_picture = request.FILES.get('profile_picture')
            
            #user.postTag = data['postTag']
            print("done")
            user.save()
            messages.add_message(
                request, messages.SUCCESS, "Your informations were successfully updated !"
            )
            return HttpResponseRedirect(reverse("users:profile", args=[username]))
        else:
            messages.add_message(
                request, messages.ERROR, "You can not update the information of someone else !"
            )
    followers = User.objects.filter(followers=user)  # user who are following this user
    return render(request, 'userProfile.html', locals())


@login_required
def logout(request):
    messages.add_message(
        request, messages.SUCCESS, "You were successfully logged out. We hope to see you soon !"
    )
    django_logout(request)
    return HttpResponseRedirect(reverse("users:login"))


@login_required
def register_tag(request):
    if request.method == "POST":
        if len(request.POST.getlist('tag')) == 0:
            messages.add_message(
                request, messages.ERROR, "You need to at least pick one tag"
            )
            return HttpResponseRedirect(reverse("feeds:front_feed"))

        for tag in request.POST.getlist('tag'):
            tag_qs = Tag.objects.filter(name=tag)
            if tag_qs.count() > 0:
                request.user.tags.add(
                    tag_qs.first()
                )
    return HttpResponseRedirect(reverse("feeds:front_feed"))

