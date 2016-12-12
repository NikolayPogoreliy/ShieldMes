from django import template
register = template.Library()
from django.shortcuts import redirect


@register.inclusion_tag('main.html')
def show_form():
    return redirect('/addpost/')