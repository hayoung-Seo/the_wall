from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register), # try register - POST
    url(r'^login$', views.login), # try login - POST
    url(r'^wall$', views.wall), # wall - html

    url(r'^post_message$', views.post_message), # post message - POST
    url(r'^delete_comment/(?P<comment_id>\d+)$', views.delete_comment), # post comment - POST
    url(r'^post_comment/(?P<message_id>\d+)$', views.post_comment), # delete comment - POST
    url(r'^logout$', views.logout),
]