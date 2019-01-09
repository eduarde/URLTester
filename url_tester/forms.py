from django import forms

from .models import Session


class SessionForm(forms.ModelForm):
    class Meta:
        model = Session
        fields = ('title', 'description',)


class SessionURLForm(forms.ModelForm):
    class Meta:
        model = Session
        fields = ('url_load',)


class SessionFormDelete(forms.ModelForm):

    class Meta:
        model = Session
        fields = []

