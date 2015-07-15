from django.conf.urls import patterns, url
from bike import views
from forms import BicycleUpdate, UserUpdate


urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^dashboard/$', views.dashboard, name='dashboard'),
	url(r'^areyousure/(?P<slug>[\w\-]+)/$', views.areyousure, name='areyousure'),
	url(r'^delete/(?P<slug>[\w\-]+)/$', views.delete, name='delete'),
	url(r'^(?P<user>[\w\-]+)_update_user/$', UserUpdate.as_view(success_url="/bike/dashboard/"), name='updateuser'),
	url(r'^(?P<slug>[\w\-]+)_update_form/$', BicycleUpdate.as_view(), name='updatebicycle'),
	url(r'^about/$', views.about, name='about'),
	url(r'^category/(?P<category_name_slug>[\w\-]+)/$', views.category, name='category'),
	url(r'^add_bicycle/$', views.add_bicycle, name='add_bicycle'),
	url(r'^search/$', views.search, name='search'),
	url(r'^add_profile/$', views.add_profile, name='add_profile'),
	url(r'^(?P<brand_model>[\w\-]+)/$', views.bicycle, name='bicycle'),
)