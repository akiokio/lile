__author__ = 'akiokio'
# -*- coding: utf-8 -*-

from django import forms
from mailer.models import Email, Queue

class LeadListForm(forms.Form):
    leadList = forms.FileField(
        label='Select a file',
        help_text='max. 42 megabytes'
    )

class EmailForm(forms.ModelForm):
    class Meta:
        model = Email
        exclude = ()

class QueueForm(forms.ModelForm):
    class Meta:
        model = Queue
        exclude = ()