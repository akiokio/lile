__author__ = 'akiokio'
# -*- coding: utf-8 -*-

import csv

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import FormView, ListView, CreateView, DetailView, View
from django.shortcuts import render_to_response, redirect
from django.contrib import messages
from django.core import mail
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt

from mailer.forms import LeadListForm, QueueForm
from mailer.models import Lead, Email, LeadContact, Queue


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
    fields = ["title", "content", ]
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

    # @transaction.atomic
    def form_valid(self, form):
        form.instance.save()
        queue = form.instance
        leadList = []
        # transaction.set_autocommit(False)
        for lead in form.cleaned_data["recipients"]:
            if lead.status == Lead.REGISTERED:
                leadList.append(LeadContact(
                    queue=queue,
                    recipient=lead,
                    _html=form.cleaned_data["email"].content,
                    _text=form.cleaned_data["email"].content,
                ))

        LeadContact.objects.bulk_create(leadList, batch_size=1000)
        # transaction.commit()
        # transaction.set_autocommit(True)
        return super(MailerCreateQueue, self).form_valid(form)


class MailerQueueList(ListView):
    template_name = "mailer_queue_list.html"
    model = Queue

    def get_context_data(self, **kwargs):
        context = super(MailerQueueList, self).get_context_data(**kwargs)
        context['total_objects'] = context['object_list'].paginator._get_count
        return context

    def get_queryset(self, *args, **kwargs):
        queryset = super(MailerQueueList, self).get_queryset()
        paginator = Paginator(queryset, 25)
        page = self.request.GET.get('page', 1)
        try:
            queryset = paginator.page(page)
        except PageNotAnInteger:
            queryset = paginator.page(1)
        except EmptyPage:
            queryset = paginator.page(paginator.num_pages)
        return queryset


class MailerQueueDetail(DetailView):
    template_name = "mailer_queue_detail.html"
    model = Queue


class MailerQueueSend(View):
    template_name = "mailer_queue_detail.html"

    def post(self, request, *args, **kwargs):
        queue = Queue.objects.get(pk=kwargs['pk'])
        connection = mail.get_connection()   # Use default email connection, open only one connection
        leadList = queue.leadcontact_set.all()
        iterateBy = 500
        for initRange in xrange(0, leadList.count(), iterateBy):
            endRange = initRange + (iterateBy - 1)
            # print('Init at: %s, End at: %s' % (initRange, endRange))
            messagesToSend = queue.getMessagesQueue(init=initRange, end=endRange)
            # print('Generated %s messages' % len(messagesToSend))
            connection.send_messages(messagesToSend)
        queue.status = Queue.SENT
        queue.save()
        messages.add_message(request, messages.SUCCESS, 'Send process started')
        return redirect('mailer_queue_detail', pk=kwargs['pk'])

@csrf_exempt
def MailerUnsubscribe(request, *args, **kwargs):
    if request.method == "POST":
        user = Lead.objects.get(email=request.POST.get('email'))
        user.status = Lead.OPTOUT
        user.save()
        context = {
            'first_name': user.first_name
        }
        return render_to_response('mailer_unsubscribe_success.html', context)