from django.conf.urls import patterns, url

from upToDate import views

urlpatterns = patterns('',
	url(r'^$', views.start, name='start'),
	url(r'^start/$', views.start, name='start'),
	url(r'^set_key/$', views.set_key, name='set_key'),
	url(r'^flickr/$', views.flickr, name='flickr'),
	url(r'^local/$', views.local, name='local'),
	url(r'^local/localTag/$', views.localTag, name='localTag'),
	url(r'^local/localImage/$', views.localImage, name='localImage'),
	url(r'^flickr/flickrTag/$', views.flickrTag, name='flickrTag'),
	url(r'^flickr/flickrImage/$', views.flickrImage, name='flickrImage'),

)