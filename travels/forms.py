from travels.models import Post, Comment
from django.forms import ModelForm


"""
Care not all the fields are present.
Still works on the website.
"""
class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['content','author','tags','location']
    def clean(self,admin=False):
        #there can be only oe occurence of a particular tag
        #size limit on content
        cleaned_data = super().clean()
        if admin :
            return
        content = cleaned_data.get('content')
        if len(content) > 150 :
            msg = "The content of this post is superior to 150 characters."
            self.add_error('content', msg)    


"""
Care not all the fields are present.
Still works on the website.

This string does not work because length of content is > 150.
{"author":1,"content":"abcdabcdab abcdabcdab abcdabcdab abcdabcdab abcdabcdab abcdabcdab abcdabcdab abcdabcdab abcdabcdab abcdabcdab abcdabcdab abcdabcdab abcdabcdab abcdabcdab ","post":1}
"""
class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['author','content','post','likes']
    def clean(self, admin=False):
        cleaned_data = super().clean()
        if admin : 
            return
        content = cleaned_data.get('content')
        if len(content) > 150 :
            msg = "The content of this comment is superior to 150 characters."
            self.add_error('content', msg)
