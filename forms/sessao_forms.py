# -*- coding: utf-8 -*-

from django.forms import ModelForm
from django import forms
from caninana.models import Sessao, PortalCatalog


class SessaoForm(ModelForm):
    url = forms.CharField(max_length=200, required=False)

    class Meta:
        model = Sessao
        fields = (
            'url', 'titulo', 'descricao', 'content_type', 'max_contents', 'status',
        )

        labels = {
            'url': 'URL',
            'titulo': 'Título',
            'descricao': 'Descrição',
            'content_type': 'Tipo de Conteúdo',
            'max_contents': 'Quantidede de máximo de conteúdo.',
            'status': 'Habilitado',
        }


class ItemSessaoForm(ModelForm):
    def __init__(self, content_type, *args, **kwargs):
        super(ItemSessaoForm, self).__init__(*args, **kwargs)
        if content_type:
            self.fields['contents'] = forms.ModelMultipleChoiceField(
                queryset=PortalCatalog.objects.filter(content_type=content_type)
            )
        else:
            self.fields['contents'] = forms.ModelMultipleChoiceField(queryset=PortalCatalog.objects.all())
    class Meta:
        model = Sessao
        fields = ['contents']
        labels = {
            'contents': 'Lista de lista de conteúdos'
        }
