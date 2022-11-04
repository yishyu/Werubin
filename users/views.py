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
        return HttpResponseRedirect(reverse("front_feed"))

    register_form = RegistrationForm()
    print("here")
    return render(request, 'registration/registration.html', locals())


def forgotpass(request):
    return render(request, 'registration/forgotpass.html', locals())
