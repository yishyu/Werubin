from django.http import HttpResponseRedirect
from django.urls import reverse


def no_user(func):
    def wrapper(*args, **kwargs):
        request = args[0]
        if not request.user.is_anonymous:
            return HttpResponseRedirect(reverse("feeds:front_feed"))
        return func(*args, **kwargs)
    return wrapper
