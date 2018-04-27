# -*- coding: utf-8 -*-

from django.forms import ModelForm
from django import forms

from caninana.models import Imagem, Organizador

class ImagemForm(ModelForm):
    url = forms.CharField(max_length=200, required=False)
    def __init__(self, *args, **kwargs):
        super(ImagemForm, self).__init__(*args, **kwargs)
        self.fields['organizador'] = forms.ModelChoiceField(required=False,
            queryset=Organizador.objects.filter(content_type='at_imagem')
        )

    class Meta:
        model = Imagem
        fields = (
            'url', 'titulo', 'descricao', 'imagem', 'categoria', 'organizador',
        )

        labels = {
            'url': 'URL.',
            'titulo':'Título do imagem.',
            'descricao':'Descrição do imagem.',
            'imagem':'Imagem.',
            'categoria':'Categoria.',
            'organizador':'Organizador de conteúdo'
        }
