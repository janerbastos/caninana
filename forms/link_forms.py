# -*- coding: utf-8 -*-

from django.forms import ModelForm
from django import forms

from caninana.models import Link, Organizador

class LinkForm(ModelForm):
    url = forms.CharField(max_length=200, required=False)
    def __init__(self, *args, **kwargs):
        super(LinkForm, self).__init__(*args, **kwargs)
        self.fields['organizador'] = forms.ModelChoiceField(required=False,
            queryset=Organizador.objects.filter(content_type='at_link')
        )

    class Meta:
        model = Link
        fields = (
            'url', 'titulo', 'descricao', 'link', 'target', 'organizador', 'categoria',
        )

        labels = {
            'url':'URL',
            'titulo':'Título da link',
            'descricao':'Descrição da link.',
            'link':'Link para',
            'target':'Opção de carregamento',
            'organizador':'Organizador de conteúdo',
            'categoria':'Categoria'
        }