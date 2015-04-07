from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    url(r'^$', include('upToDate.urls'), name=None, prefix="upToDate"),
    url(r'^uptodate/', include('upToDate.urls'), name=None, prefix="upToDate"),
    )


