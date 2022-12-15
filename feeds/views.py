from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from travels.models import Post, Tag


@login_required
def front_feed(request):
    if request.user.tags.count() == 0:
        # https://stackoverflow.com/questions/8478494/ordering-django-queryset-by-a-property
        tags = sorted(Tag.objects.all()[:30], key=lambda t: t.used_count, reverse=True)
        return render(request, 'registration/register_tag.html', locals())
    return render(request, 'feeds/feed.html')
