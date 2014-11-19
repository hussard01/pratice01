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
    url(r'^blog/$', 'blog.views.index'),
    url(r'^blog/page/(?P<page>\d+)', 'blog.views.index'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^blog/entry/(?P<entry_id>\d+)', 'blog.views.read'),
    url(r'^blog/write', 'blog.views.write'),
    url(r'^blog/add/post', 'blog.views.add_post'),
    url(r'^blog/add/comment', 'blog.views.add_comment'),
    url(r'^blog/del/comment', 'blog.views.del_comment'),
    url(r'^blog/get/comments/(?P<entry_id>\d+)', 'blog.views.get_comments'),
    url(r'login', 'blog.views.login'),
    url(r'logout', 'blog.views.logout'),    
    url(r'^$', TemplateView.as_view(template_name='index.html')),
    url(r'index/$', TemplateView.as_view(template_name='index.html')),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',{'document_root': settings.MEDIA_ROOT}),    
)+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 

