from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView

from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('dashboards.views',
 url(r'^admin/', include(admin.site.urls)),
    (r'^logged/$', TemplateView.as_view(template_name='base.html')), #render base.html when user successfully logged in
    (r'^$', 'login_form'),
    (r'^register/$', 'register_form'),
    (r'^upload/$', 'upload'),
    (r'^download/$', 'download'),
    (r'^contact/thanks/$', 'thanks'),
    (r'^contact/success/$', 'success'),
    (r'^contact/error_login/$', 'error_login'),
    (r'^contact/error_message/$', 'error_message'),
    (r'^about/$', TemplateView.as_view(template_name='about.html')), #render a help page
    (r'^contact/$', 'contact1'),
    (r'^log_out/$', 'logout'),
    (r'^my_dashboards/$', 'my_dashboards'),
    (r'^publish/$', 'publish'),
    (r'^unpublish/$', 'unpublish'),
)