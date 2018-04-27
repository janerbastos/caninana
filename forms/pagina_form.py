# -*- coding: utf-8 -*-

from django.forms import ModelForm
from django import forms

from caninana.models import Pagina, Organizador

class PaginaForm(ModelForm):

    url = forms.CharField(max_length=200, required=False)

    def __init__(self, *args, **kwargs):
        super(PaginaForm, self).__init__(*args, **kwargs)
        self.fields['organizador'] = forms.ModelChoiceField(
            queryset=Organizador.objects.filter(content_type='at_pagina'), required=False
        )

    class Meta:
        model = Pagina
        fields = (
            'url', 'titulo', 'descricao', 'corpo', 'categoria', 'organizador'
        )

        labels = {
            'url':'URL',
            'titulo':'Título da página',
            'descricao':'Descrição da página.',
            'corpo':'Corpo da página.',
            'categoria':'Escolha o papel da página.',
            'organizador': 'Agregador de conteúdo'
        }