

from django.conf.urls import url, include

urlpatterns = [
    url(r'^logout/$', 'posts.views.logout', name='logout'),
    url(r'^addpost/$', 'posts.views.addpost', name="addpost"),
    url(r'^editpost/(?P<post_id>\d+)/$', 'posts.views.editpost', name="editpost"),
    url(r'^addcoment/(?P<parent_id>\d+)/$', 'posts.views.addcoment', name="addcoment"),
    url(r'^view-posts/$', 'posts.views.posts', name="posts"),
    url(r'^$', 'posts.views.start_view', name="home"),
]