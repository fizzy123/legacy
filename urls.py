from django.conf.urls import patterns, url

from legacy import views

urlpatterns = patterns('legacy.views',
    url(r'^$', 'index', name='index'),    
    url(r'^search/$', 'results', name='results'),
    url(r'^comments/(?P<user_id>\S+)/$', 'comments', name='comments'),
    url(r'^add/(?P<user_id>\S+)/$', 'add', name='add'),
    url(r'^vote/(?P<comment_id>\S+)/$', 'vote', name='vote'),
    )
