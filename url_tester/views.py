import xmltodict
import requests
from urllib.request import urlopen
from django.views.generic import View, ListView
from django.views.generic.detail import DetailView
from .models import Session, URL, Category
from django.views.generic.edit import CreateView, DeleteView
from .forms import SessionForm, SessionFormDelete, SessionURLForm
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, get_object_or_404
import threading


class SessionsListView(ListView):
    model = Session
    context_object_name = 'sessions'
    template_name = 'url_tester/sessions_list.html'

    def get_queryset(self):
        if self.kwargs.get('category') != 'all':
            category = get_object_or_404(Category, slug=self.kwargs.get('category'))
            return Session.objects.filter(category=category).order_by('-date')
        return Session.objects.all().order_by('-date')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['categories'] = Category.objects.all()
        context['page'] = self.kwargs.get('category')
        return context


class SessionDetailView(DetailView):
    model = Session
    context_object_name = 'session'
    template_name = 'url_tester/session_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()

        context['total_urls'] = len(self.object.urls.all())
        context['total_200'] = len([x for x in self.object.urls.all() if x.code == '200'])
        context['total_301'] = len([x for x in self.object.urls.all() if x.code == '301'])
        context['total_302'] = len([x for x in self.object.urls.all() if x.code == '302'])
        context['total_404'] = len([x for x in self.object.urls.all() if x.code == '404'])
        context['total_500'] = len([x for x in self.object.urls.all() if x.code == '500'])
        return context


class SessionCreateView(CreateView):
    model = Session
    template_name = 'url_tester/create_session.html'
    success_url = reverse_lazy('sessions_list')
    form_class = SessionForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            self.object = form.save(commit=False)
            self.object.date = timezone.now()
            self.object.save()
            form.save()
            return HttpResponseRedirect(self.success_url)


class SessionDeleteView(DeleteView):
    template_name = 'url_tester/delete_session.html'
    form_class = SessionFormDelete
    success_url = reverse_lazy('sessions_list')

    def get_object(self):
        return get_object_or_404(Session, pk=self.kwargs.get('pk'))

    def get_success_url(self, **kwargs):
        return reverse('sessions_list', kwargs={'category': self.get_object().category.slug})

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(instance=self.object)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(request.POST, instance=self.object)
        if form.is_valid():
            self.object.delete()
            return HttpResponseRedirect(self.get_success_url())


class SessionLoadUrl(CreateView):
    template_name = 'url_tester/load_sitemap.html'
    form_class = SessionURLForm
    success_url = reverse_lazy('session_detail')

    def get_success_url(self, **kwargs):
        return reverse('session_detail', kwargs={'pk': self.kwargs.get('pk')})

    def get_object(self):
        return get_object_or_404(Session, pk=self.kwargs.get('pk'))

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(instance=self.object)
        return render(request, self.template_name, {'form': form})

    def loadURLS(self, url_to_load):
        file = urlopen(url_to_load)
        data = file.read()
        file.close()
        data = xmltodict.parse(data)
        url_obj = []
        for d in data['urlset']['url']:
            url = URL.objects.create()
            url.link = str(d['loc'])
            url.save()
            url_obj.append(url)

        return url_obj

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(request.POST, instance=self.object)
        if form.is_valid():
            self.object.save()
            self.object.urls.set(self.loadURLS(self.object.url_load))
            return HttpResponseRedirect(self.get_success_url())


class RunTests(View):
    template_name = 'url_tester/sessions_list.html'

    def get_object_session(self):
        return get_object_or_404(Session, pk=self.kwargs.get('pk'))

    def get_success_url(self, **kwargs):
        return reverse('session_detail', kwargs={'pk': self.kwargs.get('pk')})

    @staticmethod
    def run(session_obj):
        session_obj.loaded = False
        for url in session_obj.urls.all():
            r = requests.head(url.link)
            url.code = r.status_code
            url.save()
        session_obj.loaded = True
        session_obj.save()

    def get(self, request, *args, **kwargs):
        self.session = self.get_object_session()
        thr = threading.Thread(target=RunTests.run, args=(self.session,))
        thr.start()
        return HttpResponseRedirect(self.get_success_url())
