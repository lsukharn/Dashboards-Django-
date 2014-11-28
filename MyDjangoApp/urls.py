from django.conf.urls import patterns, include, url


from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('dashboards.views',
 url(r'^admin/', include(admin.site.urls)),
    (r'^logged/$', 'base_request'),
    (r'^$', 'login_form'),
    (r'^register/$', 'register_form'),
    (r'^upload/$', 'upload'),
    (r'^download/$', 'download'),
    (r'^contact/thanks/$', 'thanks'),
    (r'^contact/success/$', 'success'),
    (r'^contact/error_login/$', 'error_login'),
    (r'^contact/error_message/$', 'error_message'),
    (r'^about/$', 'about'),
    (r'^contact/$', 'contact1'),
    (r'^log_out/$', 'logout'),
    (r'^my_dashboards/$', 'my_dashboards'),
    (r'^publish/$', 'publish'),
    (r'^unpublish/$', 'unpublish'),
)