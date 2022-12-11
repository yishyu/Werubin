from travels.models import Post, Comment
from django.forms import ModelForm


class PostForm(ModelForm):
    """
        Care not all the fields are present.
        Still works on the website.
    """
    class Meta:
        model = Post
        fields = ['content', 'author', 'tags', 'location']

    def clean(self, admin=False):
        # there can be only oe occurence of a particular tag
        # size limit on content
        cleaned_data = super().clean()
        if admin:
            return
        content = cleaned_data.get('content')
        if len(content) > 150:
            msg = "The content of this post is superior to 150 characters."
            self.add_error('content', msg)
