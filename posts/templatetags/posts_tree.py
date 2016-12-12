from django import template
from posts.models import Posts
from django.contrib.auth import get_user

register = template.Library()

@register.inclusion_tag('posts_tree.html')
def posts_tree(post, user):
    children = Posts.objects.filter(parent=post).order_by('date')
    return {'post': post, 'children': children, 'user':user}