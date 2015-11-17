__author__ = 'akiokio'
# -*- coding: utf-8 -*-

import csv

from django.views.generic import TemplateView, FormView, ListView, CreateView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse

from mailer.forms import LeadListForm, EmailForm, QueueForm
from mailer.models import Lead, Email, LeadContact


class MailerImport(FormView):
    template_name = 'mailer_import.html'
    form_class = LeadListForm
    success_url = '/mailer/list/'

    def handle_file(self, leadListFile):
        reader = csv.DictReader(leadListFile)
        for row in reader:
            Lead.objects.update_or_create(email=row['email'], first_name=row['first_name'], last_name=row['last_name'])

    def form_valid(self, form):
        self.handle_file(self.request.FILES.get('leadList'))
        return super(MailerImport, self).form_valid(form)


class MailerList(ListView):
    template_name = 'mailer_list.html'
    model = Lead

    def get_context_data(self, **kwargs):
        context = super(MailerList, self).get_context_data(**kwargs)
        context['total_objects'] = context['object_list'].paginator._get_count
        return context

    def get_queryset(self, *args, **kwargs):
        queryset = super(MailerList, self).get_queryset().filter(status=Lead.REGISTERED)
        paginator = Paginator(queryset, 25)
        page = self.request.GET.get('page', 1)
        try:
            queryset = paginator.page(page)
        except PageNotAnInteger:
            queryset = paginator.page(1)
        except EmptyPage:
            queryset = paginator.page(paginator.num_pages)

        return queryset

class MailerCreateTemplates(CreateView):
    template_name = "mailer_create_templates.html"
    model = Email
    fields = ["title", "content", "plain_content",]
    success_url = '/mailer/template/create/'


class MailerListTemplates(ListView):
    template_name = "mailer_list_templates.html"
    model = Email

    def get_context_data(self, **kwargs):
        context = super(MailerListTemplates, self).get_context_data(**kwargs)
        context['total_objects'] = context['object_list'].paginator._get_count
        return context

    def get_queryset(self, *args, **kwargs):
        queryset = super(MailerListTemplates, self).get_queryset()
        paginator = Paginator(queryset, 25)
        page = self.request.GET.get('page', 1)
        try:
            queryset = paginator.page(page)
        except PageNotAnInteger:
            queryset = paginator.page(1)
        except EmptyPage:
            queryset = paginator.page(paginator.num_pages)
        return queryset

class MailerCreateQueue(FormView):
    template_name = "mailer_create_queue.html"
    form_class = QueueForm
    success_url = "/mailer/queue/create/"

    def form_valid(self, form):
        form.instance.save()
        queue = form.instance
        for lead in form.cleaned_data["recipients"]:
            LeadContact.objects.create(
                queue=queue,
                recipient=lead,
                _html=form.cleaned_data["email"].content,
                _text=form.cleaned_data["email"].plain_content,
            )
        return super(MailerCreateQueue, self).form_valid(form)