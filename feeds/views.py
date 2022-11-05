from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def front_feed(request):
    return render(request, 'base.html')
