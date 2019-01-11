import uuid
from django.db import models
from django.urls import reverse
from django.template.defaultfilters import slugify


class BaseModel(models.Model):
    name = models.CharField(verbose_name='Name', max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Project(BaseModel):
    color = models.CharField(verbose_name='Color Code', max_length=7, null=True, blank=True,
                             help_text='Add the desired color code. You can choose one from <a href="http://brand-colors.com/" target="_blank">here</a>')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Project, self).save(*args, **kwargs)


class Category(BaseModel):

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)


class Session(models.Model):
    title = models.CharField(verbose_name='Title', max_length=400)
    description = models.TextField(verbose_name='Description')
    date = models.DateTimeField(blank=True, null=True)
    urls = models.ManyToManyField('URL', related_name='session_url')
    url_load = models.URLField(verbose_name='URL to load', blank=True, null=True)
    loaded = models.BooleanField(blank=True, default=False)
    category = models.ForeignKey('Category', related_name='session_category', on_delete=models.SET_NULL, null=True)
    project = models.ForeignKey('Project', related_name='session_project', on_delete=models.CASCADE)
    slug = models.SlugField(max_length=100, unique=True, blank=True, default=uuid.uuid1)

    def save(self, *args, **kwargs):
        self.slug = slugify('{0} {1}'.format(self.title, self.category.name))
        super(Session, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('session_detail', kwargs={'proj': self.project.slug, 'slug': self.slug})

    def __str__(self):
        return '{0} - {1}'.format(self.title, self.category.name)


class URL(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    link = models.URLField()
    code = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return self.link
