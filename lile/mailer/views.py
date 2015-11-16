__author__ = 'akiokio'
# -*- coding: utf-8 -*-

import csv

from django.views.generic import TemplateView, FormView, ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from mailer.forms import LeadListForm
from mailer.models import Lead


class MailerImport(FormView):
    template_name = 'mailer_import.html'
    form_class = LeadListForm
    success_url = 'queue/'

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
        queryset = super(MailerList, self).get_queryset()
        paginator = Paginator(queryset, 25)

        page = self.request.GET.get('page', 1)

        try:
            queryset = paginator.page(page)
        except PageNotAnInteger:
            queryset = paginator.page(1)
        except EmptyPage:
            queryset = paginator.page(paginator.num_pages)

        return queryset