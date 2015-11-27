__author__ = 'akiokio'
# -*- coding: utf-8 -*-

"""lile URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""

from mailer.views import MailerImport, MailerList, MailerCreateTemplates, MailerListTemplates, MailerCreateQueue, \
    MailerQueueList, MailerQueueDetail, MailerQueueSend

from django.conf.urls import include, url

urlpatterns = [
    url(r'^$', MailerImport.as_view(), name='mailer_import'),
    url(r'^list/$', MailerList.as_view(), name='mailer_list'),
    url(r'^template/create/$', MailerCreateTemplates.as_view(), name='mailer_create_templates'),
    url(r'^template/list/$', MailerListTemplates.as_view(), name='mailer_list_templates'),
    url(r'^queue/create/$', MailerCreateQueue.as_view(), name='mailer_create_queue'),
    url(r'^queue/list/$', MailerQueueList.as_view(), name='mailer_queue_list'),
    url(r'^queue/detail/(?P<pk>[-\w]+)/$', MailerQueueDetail.as_view(), name='mailer_queue_detail'),


    url(r'^queue/send/(?P<pk>[-\w]+)/$', MailerQueueSend.as_view(), name='mailer_queue_send'),
]