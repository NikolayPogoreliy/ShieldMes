from django.forms import ModelForm
from posts.models import Posts


class PostForm(ModelForm):
    class Meta():
        model = Posts
        fields = ['title', 'text']


class ComentForm(ModelForm):
    class Meta():
        model = Posts
        fields = ['text']
