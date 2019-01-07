from django.shortcuts import render
from django.views.generic import View, ListView
from django.views.generic.detail import DetailView
from .models import Session, URL



class SessionsListView(ListView):

    model = Session
    context_object_name = 'sessions'
    template_name = 'url_tester/sessions_list.html'

    def get_queryset(self):
        return Session.objects.all().order_by('date')


class SessionDetailView(DetailView):

    model = Session
    context_object_name = 'session'
    template_name = 'url_tester/session_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        return context

