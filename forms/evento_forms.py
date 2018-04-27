# -*- coding: utf-8 -*-

from django.forms import ModelForm
from django import forms

from caninana.models import Evento

class EventoForm(ModelForm):
    url = forms.CharField(max_length=200, required=False)
    class Meta:
        model = Evento
        fields = (
            'url', 'titulo', 'descricao', 'favico', 'logo', 'template'
        )
        labels = {
            'url':'URL do Evento',
            'titulo':'Titulo do Evento',
            'descricao':'Descrição do evento',
            'favico':'Favico',
            'logo':'Logo',
            'template':'Template do Site'
        }