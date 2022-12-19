from travels.models import Post


def validate_post(request):
    """
        Validate an Add post request
    """
    errors = {
        "Missing Keys": [],
        "Others": []
    }
    status = True

    # Address
    if not request.data.get("googleAddress"):
        status = False
        errors["Missing Keys"].append("googleAddress")
    try:
        float(request.data["lat"])
        float(request.data["lng"])
    except ValueError:
        status = False
        errors["Others"].append("Coordinate points have to be float")
    except KeyError:
        status = False
        errors["Missing Keys"].append("lat | lng")

    # Content
    if not request.data.get("content"):
        status = False
        errors["Missing Keys"].append("content")
    else:
        if len(request.data["content"]) > Post.MAX_LENGTH:
            status = False
            errors['Others'].append(f"A Post content has a limited size of {Post.MAX_LENGTH} characters")

    # Tag
    if sum([1 if "postTag" in key else 0 for key in request.data.keys()]) == 0:
        status = False
        errors['MissingKeys'].append("PostTag. If you wish to have many tags, you need to create an indexing: PostTag1, PostTag2, PostTag3,...")

    return status, errors
