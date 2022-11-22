from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def front_feed(request):
    return render(request, 'base.html')

@login_required
def singlePost(request, postID):

    # example variables
    username = "Tristan Cazier"
    postID=1000
    location="Egypt"
    hashtags="#Egypt, #Mummy, #Pyramids"
    profilepicture="https://cdn.discordapp.com/avatars/238355399634321408/a_0deed0f2ae15f2c36417675403066ddf.gif?size=1024"
    picturelink="https://i.pinimg.com/736x/90/6f/99/906f99062b11c79e64f30c4a6be37ba3.jpg"
    map=""
    posttext="Looking for mummies"
    numberofcomments=1
    posttime="2 November 2022, 22:12"
    

    return render(request, 'posts/singlepostpage.html', locals())