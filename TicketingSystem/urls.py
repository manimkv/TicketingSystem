from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'ticket.views.signin'),    
    url(r'^accounts/login/$', 'ticket.views.signin'),
    url(r'^login/$', 'ticket.views.login_view'),    
    url(r'^logout/$', 'ticket.views.logout_view'),
    url(r'^dashboard/$', 'ticket.views.dashboard'), 
    url(r'^fetch_tickets/$', 'ticket.views.fetch_tickets'), 
    url(r'^search_tickets/$', 'ticket.views.search_tickets'), 
    url(r'^ticket_action/$', 'ticket.views.ticket_action'), 
    url(r'^filter_tickets/$', 'ticket.views.filter_tickets'), 
)
