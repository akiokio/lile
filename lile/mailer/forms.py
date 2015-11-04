__author__ = 'akiokio'
# -*- coding: utf-8 -*-

from django import forms

class LeadListForm(forms.Form):
    leadList = forms.FileField(
        label='Select a file',
        help_text='max. 42 megabytes'
    )