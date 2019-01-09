from django.db import models
from django.urls import reverse
import requests


class SessionURLS(models.Model):
    url = models.ForeignKey('URL', related_name='url', on_delete=models.CASCADE)
    session = models.ForeignKey('Session', related_name='session_urls', on_delete=models.CASCADE)
    code = models.CharField(max_length=10, null=True, blank=True)

    class Meta:
        auto_created = True
        verbose_name = 'Session URL'
        verbose_name_plural = 'Sessions URL'

    def __str__(self):
        return '{0} {1} {2}'.format(self.session.title, self.url.link, self.code)


class Session(models.Model):
    title = models.CharField(max_length=400)
    description = models.TextField()
    date = models.DateTimeField(blank=True, null=True)
    urls = models.ManyToManyField('URL', related_name='session_url', through=SessionURLS, null=True, blank=True)
    url_load = models.URLField(blank=True, null=True)

    def get_absolute_url(self):
        return reverse('session_detail', args=[self.pk])

    def __str__(self):
        return self.title


class URL(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    link = models.URLField()

    def __str__(self):
        return self.link
