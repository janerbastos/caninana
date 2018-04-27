# -*- coding: utf-8 -*-

from django.forms import ModelForm
from django import forms

from caninana.models import Menu

class MenuForm(ModelForm):
    url = forms.CharField(max_length=200, required=False)

    class Meta:
        model = Menu
        fields = (
           'url', 'titulo', 'link', 'status',
        )

        labels = {
            'url':'URL.',
            'titulo':'Título',
            'link':'Encaminhar para',
            'Status':'Habilitar'
        }