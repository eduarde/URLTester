from django.db import models
from django.urls import reverse
from django.template.defaultfilters import slugify


class Category(models.Model):
    name = models.CharField(verbose_name='Name', max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Session(models.Model):
    title = models.CharField(verbose_name='Title', max_length=400)
    description = models.TextField(verbose_name='Description')
    date = models.DateTimeField(blank=True, null=True)
    urls = models.ManyToManyField('URL', related_name='session_url')
    url_load = models.URLField(verbose_name='URL to load', blank=True, null=True)
    loaded = models.BooleanField(blank=True, default=False)
    category = models.ForeignKey('Category', related_name='session_category', on_delete=models.SET_NULL, null=True)

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
