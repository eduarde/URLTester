from django import forms

from .models import Session, Project


class SessionForm(forms.ModelForm):
    class Meta:
        model = Session
        fields = ('title', 'description', 'category',)


class SessionURLForm(forms.ModelForm):
    class Meta:
        model = Session
        fields = ('url_load',)


class SessionFormDelete(forms.ModelForm):
    class Meta:
        model = Session
        fields = []


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('name', 'color',)
