from django.conf.urls import patterns, include, url
from django.views.generic.simple import direct_to_template
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'store.views.home', name='home'),
    # url(r'^store/', include('store.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
   url(r'^admin/', include(admin.site.urls)),
   (r'^$', direct_to_template, {'template': 'index.html'}),
   (r'^products/$', 'webstore.views.ProductsAll'),
   (r'^products/(?P<productslug>.*)/$', 'webstore.views.SpecificProduct'),
   (r'^events/$', 'webstore.views.EventsAll'),
   (r'^events/(?P<categoryslug>.*)/$', 'webstore.views.Category'),
   (r'^singleevent/(?P<eventslug>.*)/$', 'webstore.views.SpecificEvent'),
   (r'^cart/$', 'webstore.views.Cart'),
   (r'^search/$', 'webstore.views.Search'),

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 

urlpatterns += staticfiles_urlpatterns()
