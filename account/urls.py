from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^edit_info/',views.edit_info,name='edit_info'),
    # /profile/
    url(r'^$',views.index, name='index'),


]
