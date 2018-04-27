# -*- coding: utf-8 -*-

from django.forms import ModelForm
from django import forms

from caninana.models import Agenda, Organizador

class AgendaForm(ModelForm):
    url = forms.CharField(max_length=200, required=False)
    def __init__(self, *args, **kwargs):
        super(AgendaForm, self).__init__(*args, **kwargs)
        self.fields['organizador'] = forms.ModelChoiceField(required=False,
            queryset=Organizador.objects.filter(content_type='at_agenda')
        )

    class Meta:
        model = Agenda
        fields = (
            'url', 'titulo', 'descricao', 'corpo', 'inicio_at', 'termino_at', 'organizador', 'categoria'
        )

        labels = {
            'url': 'URL',
            'titulo':'Título da agenda',
            'descricao':'Descrição da agenda.',
            'corpo':'Corpo da agenda.',
            'inicio_at':'Início da programação',
            'termino_at':'Termino da programação',
            'organizador':'Organizador de conteúdo',
            'categoria':'Categoria da agenda.',
        }