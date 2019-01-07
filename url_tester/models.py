from django.db import models
from django.urls import reverse
import requests


class Session(models.Model):
    title = models.CharField(max_length=400)
    description = models.TextField()
    date = models.DateTimeField(blank=True, null=True)
    urls = models.ManyToManyField('URL', related_name='session_url')

    def get_absolute_url(self):
        return reverse('session_detail', args=[self.pk])

    def __str__(self):
        return self.title


class URL(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    link = models.URLField()
    code = models.CharField(max_length=10, null=True, blank=True)

    @property
    def status(self):
        r = requests.head(self.link)
        self.code = r.status_code

        if r.status_code == 200:
            return 'success'

        if r.status_code == 301:
            return 'warning'
        return 'danger'

    def __str__(self):
        return self.link
