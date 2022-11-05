from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView
from users.forms import RegistrationForm
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login as Login


# Sign Up View
def registration(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            print("form is valid")
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
    return render(request, 'registration/forgotpass.html', locals())
