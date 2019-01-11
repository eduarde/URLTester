from django.contrib import admin
from .models import Session, URL, Category, Project

admin.site.register(Session)
admin.site.register(URL)
admin.site.register(Category)
admin.site.register(Project)
