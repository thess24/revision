from django.conf.urls import patterns, url
from eyes import views



urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^home/$', views.home, name='home'),   
    url(r'^additem/$', views.additem, name='additem'),
    url(r'^addproject/$', views.addproject, name='addproject'),
    url(r'^(?P<projectname>.+)/announce/$', views.announce, name='announce'),        
    url(r'^(?P<projectname>.+)/$', views.projectpage, name='projectpage'),
)
