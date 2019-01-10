from django.db import models
from django.urls import reverse


class Session(models.Model):
    title = models.CharField(verbose_name='Title', max_length=400)
    description = models.TextField(verbose_name='Description')
    date = models.DateTimeField(blank=True, null=True)
    urls = models.ManyToManyField('URL', related_name='session_url')
    url_load = models.URLField(verbose_name='URL to load', blank=True, null=True)
    loaded = models.BooleanField(blank=True, default=False)
    type = models.CharField(verbose_name='Type', max_length=400, blank=True, null=True)

    def get_absolute_url(self):
        return reverse('session_detail', args=[self.pk])

    def __str__(self):
        return self.title


class URL(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    link = models.URLField()
    code = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return self.link
