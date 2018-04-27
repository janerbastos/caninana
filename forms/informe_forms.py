# -*- coding: utf-8 -*-

from django.forms import ModelForm
from django import forms

from caninana.models import Informe, Organizador

class InformeForm(ModelForm):
    url = forms.CharField(max_length=200, required=False)
    def __init__(self, *args, **kwargs):
        super(InformeForm, self).__init__(*args, **kwargs)
        self.fields['organizador'] = forms.ModelChoiceField(required=False,
            queryset=Organizador.objects.filter(content_type='at_informe')
        )

    class Meta:
        model = Informe
        fields = (
            'url', 'titulo', 'descricao', 'corpo', 'imagem', 'categoria', 'organizador'
        )

        labels = {
            'url': 'URL',
            'titulo':'Título do informe',
            'descricao':'Descrição do informe.',
            'corpo':'Corpo da informe.',
            'imagem': 'Imagem de destaque.',
            'categoria':'Escolha o papel da informe.',
            'organizador': 'Agregador de conteúdo'
        }
