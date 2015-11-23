__author__ = 'akiokio'
# -*- coding: utf-8 -*-

from django.db import models
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template import Context, Template

from smtplib import SMTPException


class CreationMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Lead(CreationMixin):
    REGISTERED = '1'
    OPTOUT = '2'

    LEAD_STATUS = (
        (REGISTERED, 'Registered'),
        (OPTOUT, 'Opt-out'),
    )
    email = models.EmailField(max_length=254, unique=True, primary_key=True)
    first_name = models.CharField(max_length=254)
    last_name = models.CharField(max_length=254)

    status = models.CharField(max_length=1, choices=LEAD_STATUS, default=1)

    def __unicode__(self):
        return self.email


class Email(CreationMixin):
    title = models.CharField(max_length=500)
    content = models.TextField()
    plain_content = models.TextField()

    def __unicode__(self):
        return self.title


class Queue(CreationMixin):
    title = models.CharField(max_length=254)

    email = models.ForeignKey(Email)
    recipients = models.ManyToManyField(Lead, through='LeadContact')

    def __unicode__(self):
        return self.title


class LeadContact(CreationMixin):
    PENDING = 1
    SENT = 2
    BOUNCED = 3
    OPENED = 4
    SEND_ERROR = 5

    LEAD_CONTACT_STATUS = (
        (PENDING, 'Pending'),
        (SENT, 'Sent'),
        (BOUNCED, 'Bounced'),
        (OPENED, 'Opened'),
        (SEND_ERROR, 'Send error')
    )

    queue = models.ForeignKey(Queue)
    recipient = models.ForeignKey(Lead)

    status = models.CharField(max_length=254, choices=LEAD_CONTACT_STATUS, default=1)
    _html = models.TextField()
    _text = models.TextField()
    obs = models.TextField()

    def __unicode__(self):
        return '%s - %s' % (self.queue, self.recipient)

    def html(self, template, context):
        template = Template(self.email.content)
        self._html = template.render(Context(context))


    def text(self, template, context):
        template = Template(self.email.content)
        self._text = template.render(Context(context))


    def send(self, from_addr=None):
        if isinstance(self.recipient.email, basestring):
            toEmail = [self.recipient.email]
        else:
            toEmail = self.recepient.email
        if not from_addr:
            from_addr = getattr(settings, 'EMAIL_FROM_ADDR')
        msg = EmailMultiAlternatives(
            self.queue.email.title,
            self._text,
            from_addr,
            toEmail
        )
        if self._html:
            msg.attach_alternative(self._html, 'text/html')
        try:
            msg.send()
            self.status = 2
            self.obs += "\n message sent"
        except SMTPException as e:
            self.status = 5
            self.obs = e.message
        self.save()
