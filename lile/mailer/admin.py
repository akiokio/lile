from django.contrib import admin

from mailer.models import Lead, Email, Queue, LeadContact

class LeadsContactInline(admin.TabularInline):
	model = Queue.recipients.through


class QueueAdmin(admin.ModelAdmin):
	inlines = [LeadsContactInline,]


admin.site.register(Lead)
admin.site.register(Email)
admin.site.register(Queue, QueueAdmin)
admin.site.register(LeadContact)