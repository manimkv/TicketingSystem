from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'TicketingSystem.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'ticket.views.signin'),    
    url(r'^accounts/login/$', 'ticket.views.signin'),
    url(r'^login/$', 'ticket.views.login_view'),    
    url(r'^logout/$', 'ticket.views.logout_view'),
    url(r'^dashboard/$', 'ticket.views.dashboard'), 
    url(r'^fetch_tickets/$', 'ticket.views.fetch_tickets'), 
    url(r'^sort_tickets/$', 'ticket.views.sort_tickets'), 

)
