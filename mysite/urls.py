from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.views.generic.base import TemplateView

admin.autodiscover()

import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


urlpatterns = patterns('',
    # Examples:
    # url(rd'^$', 'mysite.views.home', name='home'),
        #admin
    url(r'^admin/', include(admin.site.urls)),
    
    #basic
    url(r'index/$', TemplateView.as_view(template_name='index.html')),
    url(r'^$', TemplateView.as_view(template_name='index.html')),
    
    #blog
    url(r'^blog/$', 'blog.views.list'),
    url(r'^blog/(?P<blogid>[^\/]+)/$', 'blog.views.list'),
    url(r'^blog/(?P<blogid>[^\/]+)/page/(?P<page>\d+)/$', 'blog.views.list'),
    url(r'^blog/(?P<blogid>[^\/]+)/entry/(?P<entry_id>\d+)/$', 'blog.views.read'),
    url(r'^blog/(?P<blogid>[^\/]+)/write/$', 'blog.views.write'),
    #url(r'^blog/write', 'blog.views.write'),
    url(r'^blog/(?P<blogid>[^\/]+)/add/post', 'blog.views.add_post'),
    url(r'^blog/(?P<blogid>[^\/]+)/update/form/(?P<entry_id>\d+)/$', 'blog.views.updateform'),
    url(r'^blog/(?P<blogid>[^\/]+)/update/post/(?P<entry_id>\d+)/$', 'blog.views.update_post'),    
    url(r'^blog/(?P<blogid>[^\/]+)/del/post/(?P<entry_id>\d+)/$', 'blog.views.del_post'),
    #url(r'^blog/add/post', 'blog.views.add_post'),
    url(r'^blog/add/comment', 'blog.views.add_comment'),
    url(r'^blog/del/comment', 'blog.views.del_comment'),
    url(r'^blog/get/comments/(?P<entry_id>\d+)', 'blog.views.get_comments'),
       
    #join
    url(r'join_form', 'blog.views.joinform'),
    url(r'join', 'blog.views.join'),
    
    #login
    url(r'login/form/$', 'blog.views.loginform'),
        #url(r'login_form\?next=(?P<next>.+)/$', 'blog.views.loginform'),
    url(r'login/action', 'blog.views.loginAction'),
    url(r'logout/action', 'blog.views.logout'),
    url(r'login/profile', 'blog.views.profile'),

    #allauth
    (r'^accounts/', include('allauth.urls')),
    (r'^accounts/profile', 'blog.views.profile'),

            
    #img, video    
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',{'document_root': settings.MEDIA_ROOT}),        

    #file browser    
    url(r'^redactor/', include('redactor.urls')),
        
    #search 
    url(r'^search/', include('haystack.urls')),
    url(r'^search/form', 'blog.views.searchAction'),



)+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 

