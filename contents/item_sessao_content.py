# -*- coding: utf-8 -*-

from django.shortcuts import redirect, render, get_object_or_404
from django.http import Http404, JsonResponse
from django.template.loader import render_to_string
from django.utils.text import slugify

from caninana.models import SessaoContents, Sessao
from caninana.contents import portal_catalog_content

import datetime
import json

from caninana.forms.sessao_forms import ItemSessaoForm

from caninana.models import PortalCatalog

TEMPLATE = 'caninana/comum/%s.html'
CONTENT_TYPE = 'at_item_sessao'


def create(request, **kwargs):

    sessao = kwargs.get('sessao', None)
    content_type = sessao.content_type
    result = sessao.contents.all().values_list('url', flat=True)
    portal_catalog = PortalCatalog.objects.filter(evento=sessao.evento)
    if content_type:
        portal_catalog = portal_catalog.filter(content_type=content_type)

    portal_catalog = portal_catalog.exclude(content_type__in=('at_menu', 'at_sessao', 'at_organizador'))
    portal_catalog = portal_catalog.exclude(url__in=result)

    if request.method == 'POST':
        list = request.POST.getlist('itens_sessao')
        contador = sessao.contents.count()
        for uid in list:
            if contador == sessao.max_contents:
                break;
            pc = PortalCatalog.objects.get(evento=sessao.evento, url=uid)
            sc = SessaoContents(sessao=sessao, portal_catalog=pc)
            sc.save()
            contador += 1

        return redirect(sessao.evento.get_absolute_url()+'?@@list=at_sessao')

    html = render_to_string('caninana/includes/ajax/conteudo_auxiliar.html', {'objects': portal_catalog, 'opcao': 'at_item_sessao'})

    data = {
        'result': html,
        'sessao': sessao.titulo,
    }
    return JsonResponse(data)


def remove(request, **kwargs):
    sessao = kwargs.get('sessao', None)
    contents = sessao.contents.all()

    if request.method == 'POST':
        list = request.POST.getlist('itens_sessao')
        for uid in list:
            pc = PortalCatalog.objects.get(evento=sessao.evento, url=uid)
            sc = SessaoContents.objects.get(sessao=sessao, portal_catalog=pc)
            sc.delete()

        return redirect(sessao.evento.get_absolute_url() + '?@@list=at_sessao')

    html = render_to_string('caninana/includes/ajax/conteudo_auxiliar.html', {'objects': contents, 'opcao': 'at_item_sessao'})
    data = {
        'result' : html,
        'sessao' : sessao.titulo,
    }

    return JsonResponse(data)


def view(request, evento, sessao_id, action=None):

    sessao = get_object_or_404(Sessao, url=sessao_id)
    content_type = request.GET.get('createObject', None)

    if action == 'remover':
        return remove(request, sessao=sessao)
    else:
        return create(request, sessao=sessao, content_type=content_type)

