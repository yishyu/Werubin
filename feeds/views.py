from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from travels.models import Post, Tag
from django.shortcuts import get_object_or_404


@login_required
def front_feed(request):
    """
        Front feed is shown when a user logs in
    """
    # if the user has no tags, show him the register tag page
    if request.user.tags.count() == 0:
        # https://stackoverflow.com/questions/8478494/ordering-django-queryset-by-a-property
        tags = sorted(Tag.objects.all()[:30], key=lambda t: t.used_count, reverse=True)
        return render(request, 'registration/registerTag.html', locals())
    return render(request, 'feeds/feed.html')


@login_required
def tag_feed(request, tagName):
    """
        This view is used to display a feed of posts with a specific tag
    """
    tag = get_object_or_404(Tag, name=tagName)
    return render(request, 'feeds/tagFeed.html', locals())
