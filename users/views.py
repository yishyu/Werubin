from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView
from users.forms import RegistrationForm
from django.http import HttpResponseRedirect


# Sign Up View
def registration(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            print("form is valid")
            user = form.save()
            user.set_password(form.cleaned_data['password1'])
            user.email =
            user.save()
            return HttpResponseRedirect(reverse("feeds:front_feed"))
        else:
            print(form.errors.items())
    return render(request, 'registration/registration.html', locals())


def forgotpass(request):
    return render(request, 'registration/forgotpass.html', locals())
