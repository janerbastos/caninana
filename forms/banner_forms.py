# -*- coding: utf-8 -*-

from django.forms import ModelForm
from django import forms

from caninana.models import Banner, Organizador

class BannerForm(ModelForm):
    url = forms.CharField(max_length=200, required=False)
    def __init__(self, *args, **kwargs):
        super(BannerForm, self).__init__(*args, **kwargs)
        self.fields['organizador'] = forms.ModelChoiceField( required=False,
            queryset=Organizador.objects.filter(content_type='at_banner')
        )

    class Meta:
        model = Banner
        fields = (
            'url', 'titulo', 'descricao', 'imagem', 'link', 'target', 'organizador', 'categoria',
        )

        labels = {
            'url': 'URL.',
            'titulo':'Título do banner.',
            'descricao':'Descrição do banner.',
            'imagem':'Imagem de apresentação.',
            'link':'Link para.',
            'target':'Opção de carregamento.',
            'organizador':'Organizador de conteúdo',
            'categoria':'Categoria.',
        }
