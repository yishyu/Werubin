from django.http import HttpResponseRedirect
from django.urls import reverse


def no_user(func):
    """
        This decorator is used to redirect a user to the front feed if he is logged in
        It is put on authentication views so that a logged in user can't access them
    """
    def wrapper(*args, **kwargs):
        request = args[0]
        if not request.user.is_anonymous:
            return HttpResponseRedirect(reverse("feeds:front_feed"))
        return func(*args, **kwargs)
    return wrapper
