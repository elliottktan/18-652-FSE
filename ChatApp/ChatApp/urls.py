from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^chatapp$', 'ChatApp.views.display'),
    url(r'^chatapp/$', 'ChatApp.views.display'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^chatapp/login$', 'django.contrib.auth.views.login', {'template_name':'chatapp/login.html'}),
    url(r'^chatapp/logout$', 'django.contrib.auth.views.logout', {'next_page':'/chatapp'}),
    url(r'^chatapp/register$', 'ChatApp.views.register'),
    url(r'^chatapp/post$', 'ChatApp.views.post'),
    url(r'^chatapp/get_posts$', 'ChatApp.views.getPosts'),
)
