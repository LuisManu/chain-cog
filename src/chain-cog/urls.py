from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from registration.backends.simple.views import RegistrationView


class MyRegistrationView(RegistrationView):
    def get_success_url(self, request, user):
        return '/bike/add_profile/'


urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'bike.views.index', name='index'),
    url(r'^bike/', include('bike.urls')),
    url(r'^accounts/register/$', MyRegistrationView.as_view(), name='registration_register'),
    (r'^accounts/', include('registration.backends.simple.urls')),
    url(r'^likes/', include('phileo.urls')),
    (r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^(?P<user_name>[\w\-.+@]+)/$', 'bike.views.profile', name='profile'),
)


if settings.DEBUG:
	urlpatterns += patterns(
		'django.views.static',
		(r'media/(?P<path>.*)',
		'serve',
		{'document_root': settings.MEDIA_ROOT}), )
