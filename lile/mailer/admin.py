__author__ = 'akiokio'
# -*- coding: utf-8 -*-

from django.contrib import admin
from mailer.models import Lead, Email, Queue, LeadContact


class LeadAdmin(admin.ModelAdmin):
    search_fields = ['email', 'first_name', 'last_name']
    list_display = ['email', 'first_name', 'last_name']

class LeadsContactInline(admin.TabularInline):
    model = Queue.recipients.through

    extra = 0
    max_num = 0


class QueueAdmin(admin.ModelAdmin):
    inlines = [LeadsContactInline, ]
    search_fields = ['title', 'status']
    list_display = ['title', 'status']

admin.site.register(Lead, LeadAdmin)
admin.site.register(Email)
admin.site.register(Queue, QueueAdmin)
admin.site.register(LeadContact)
