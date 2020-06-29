from django import forms
from .models import Post

class CreateBlog(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'body', 'image']


class UpdateBlog(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'body', 'image']

        def save(self, commit=True):
            post = self.instance
            post.title = self.cleaned_data['title']
            post.body = self.cleaned_data['body']

            if self.cleaned_data['image']:
                post.image = self.cleaned_data['image']
            if commit:
                post.save()
            return post
