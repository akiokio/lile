__author__ = 'akiokio'
# -*- coding: utf-8 -*-

from django.db import models
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
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
    
    def __unicode__(self):
        return self.title


class Queue(CreationMixin):
    PENDING = '1'
    SENT = '2'
    LEAD_CONTACT_STATUS = (
        (PENDING, 'Pending'),
        (SENT, 'Sent'),
    )

    title = models.CharField(max_length=254)
    status = models.CharField(max_length=254, choices=LEAD_CONTACT_STATUS, default=1)

    email = models.ForeignKey(Email)
    recipients = models.ManyToManyField(Lead, through='LeadContact')

    def __unicode__(self):
        return self.title

    def getMessagesQueue(self):
        emailQueue = []

        for leadContact in self.leadcontact_set.all():
            if leadContact.status == Lead.REGISTERED:
                emailQueue.append(leadContact.createMessage())

        return emailQueue


class LeadContact(CreationMixin):
    PENDING = '1'
    SENT = '2'
    BOUNCED = '3'
    OPENED = '4'
    SEND_ERROR = '5'

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

    def html(self, context):
        template = Template(self._html)
        return template.render(Context(context))

    def text(self, context):
        template = Template(self._text)
        return strip_tags(template.render(Context(context)))

    def createMessage(self, from_addr=None):
        if isinstance(self.recipient.email, basestring):
            toEmail = [self.recipient.email]
        else:
            toEmail = self.recepient.email
        if not from_addr:
            from_addr = getattr(settings, 'EMAIL_FROM_ADDR')

        contextDict = Context({'clientName': self.recipient.first_name})

        msg = EmailMultiAlternatives(
            self.queue.email.title,
            self.text(contextDict),
            from_addr,
            toEmail
        )
        msg.attach_alternative(self.html(contextDict), 'text/html')

        return msg

    def send(self, from_addr=None):
        msg = self.createMessage(from_addr=from_addr)
        try:
            msg.send()
            self.status = 2
            self.obs += "\n message sent"
        except SMTPException as e:
            self.status = 5
            self.obs = e.message
        self.save()

