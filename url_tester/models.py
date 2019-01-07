from django.db import models


class Session(models.Model):
    title = models.CharField(max_length=400)
    description = models.TextField()
    run_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.title


# Create your models here.
class URL(models.Model):
    name = models.CharField(max_length=200, null=True)
    link = models.URLField()
    session = models.ForeignKey('Session', related_name='url_session', on_delete=models.CASCADE)

    def __str__(self):
        return self.link
