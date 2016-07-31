from django.conf.urls import url 

from . import views 

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^subs/([a-z]+)/([a-z]+)', views.send_data, name="send_data")
    ]
