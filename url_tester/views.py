import xmltodict
import requests
from urllib.request import urlopen
from django.views.generic import View, ListView
from django.views.generic.detail import DetailView
from .models import Session, URL, Category, Project
from django.views.generic.edit import CreateView, DeleteView
from .forms import SessionForm, SessionFormDelete, SessionURLForm, ProjectForm
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, get_object_or_404
import threading


class HomeView(ListView):
    model = Project
    context_object_name = 'projects'
    template_name = 'url_tester/home.html'


class SessionsListView(ListView):
    model = Session
    context_object_name = 'sessions'
    template_name = 'url_tester/sessions_list.html'

    def get_project(self):
        return get_object_or_404(Project, slug=self.kwargs.get('proj'))

    def get_category(self):
        return get_object_or_404(Category, slug=self.kwargs.get('category'))

    def get_queryset(self):
        proj = self.get_project()
        if self.kwargs.get('category') != 'all':
            return Session.objects.filter(project=proj, category=self.get_category()).order_by('-date')
        return Session.objects.filter(project=proj).order_by('-date')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['project'] = self.get_project()
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
    form_class = SessionForm

    def get_success_url(self, **kwargs):
        return reverse_lazy('sessions_list', kwargs=({'category': 'all', 'proj': self.kwargs.get('proj')}))

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def get_project(self):
        return get_object_or_404(Project, slug=self.kwargs.get('proj'))

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            self.object = form.save(commit=False)
            self.object.project = self.get_project()
            self.object.date = timezone.now()
            self.object.save()
            form.save()
            return HttpResponseRedirect(self.get_success_url())


class SessionDeleteView(DeleteView):
    template_name = 'url_tester/delete_session.html'
    form_class = SessionFormDelete

    def get_object(self):
        return get_object_or_404(Session, slug=self.kwargs.get('session'))

    def get_project(self):
        return get_object_or_404(Project, slug=self.kwargs.get('proj'))

    def get_success_url(self, **kwargs):
        return reverse_lazy('sessions_list', kwargs=({'category': 'all', 'proj': self.kwargs.get('proj')}))

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
        return reverse('session_detail',
                       kwargs={'proj': self.kwargs.get('proj'), 'slug': self.kwargs.get('session')})

    def get_object(self):
        return get_object_or_404(Session, slug=self.kwargs.get('session'))

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(instance=self.object)
        return render(request, self.template_name, {'form': form})

    def loadURLS(self, object):
        file = urlopen(object.url_load)
        data = file.read()
        file.close()
        data = xmltodict.parse(data)
        for d in data['urlset']['url']:
            url = URL()
            url.link = str(d['loc'])
            url.save()
            object.urls.add(url)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(request.POST, instance=self.object)
        if form.is_valid():
            self.object.date = timezone.now()
            self.object.save()
            self.loadURLS(self.object)
            return HttpResponseRedirect(self.get_success_url())


class RunTests(View):
    template_name = 'url_tester/sessions_list.html'

    def get_object_session(self):
        return get_object_or_404(Session, slug=self.kwargs.get('session'))

    def get_success_url(self, **kwargs):
        return reverse_lazy('session_detail',
                            kwargs={'proj': self.kwargs.get('proj'), 'slug': self.kwargs.get('session')})

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


class ProjectCreateView(CreateView):
    model = Session
    template_name = 'url_tester/create_project.html'
    success_url = reverse_lazy('home')
    form_class = ProjectForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            self.object = form.save(commit=True)
            self.object.save()
            return HttpResponseRedirect(self.success_url)
