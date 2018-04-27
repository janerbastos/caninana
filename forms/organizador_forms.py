# -*- coding: utf-8 -*-

from django.forms import ModelForm
from django import forms

from caninana.models import Organizador

class OrganizadorForm(ModelForm):
    url = forms.CharField(max_length=200, required=False)

    class Meta:
        model = Organizador
        fields = (
           'url', 'titulo', 'content_type', 'status',
        )

        labels = {
            'url':'URL.',
            'titulo':'Título',
            'content_type':'Tipo de Conteúdo',
            'Status':'Habilitar'
        }