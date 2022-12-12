from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from travels.models import Post, Tag


@login_required
def front_feed(request):
    return render(request, 'feeds/feed.html')
