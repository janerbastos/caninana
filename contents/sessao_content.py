# -*- coding: utf-8 -*-

from django.shortcuts import redirect, render
from django.http import Http404
from django.utils.text import slugify

from caninana.forms.sessao_forms import SessaoForm
from caninana.models import Sessao
from caninana.contents import portal_catalog_content

import datetime

TEMPLATE = 'caninana/comum/%s.html'
CONTENT_TYPE = 'at_sessao'


def create(request, evento):
    template = TEMPLATE % 'forms'
    form = SessaoForm(request.POST or None, instance=None)
    if form.is_valid():
        sessao = form.save(commit=False)
        sessao.evento = evento
        sessao.save()
        portal_catalog_content.create(sessao, CONTENT_TYPE)
        return redirect('eventweb:index', _evento=sessao.evento.url, _content=sessao.url)
    context = {
        'form': form,
        'content_type': CONTENT_TYPE,
        'page_header': 'Nova Sessao',
        'subtext': '',
        'action': 'create',
        'evento': evento,
    }
    return render(request, template, context)


def update(request, sessao):
    template = TEMPLATE % 'forms'
    _url = sessao.url
    form = SessaoForm(request.POST or None, instance=sessao)
    if form.is_valid():
        sessao = form.save(commit=False)
        sessao.save()
        portal_catalog_content.update(sessao, _url)
        return redirect('eventweb:index', _evento=sessao.evento.url, _content=sessao.url)
    context = {
        'object': sessao,
        'form': form,
        'content_type': CONTENT_TYPE,
        'page_header': 'Atualizando sessão',
        'subtext': '',
        'action': 'update',
        'evento': sessao.evento,
    }
    return render(request, template, context)


def view(request, evento, sessao_url, listar=False):
    template = TEMPLATE % 'sessoes'
    action = request.GET.get('action', None)
    sessoes = None
    sessao = None
    page_header = None
    try:
        if listar:
            sessoes = Sessao.objects.filter(evento=evento)
            page_header = 'Lista de Sessões'
        else:
            sessao = Sessao.objects.get(evento=evento, url=sessao_url)
            page_header = sessao.titulo
        if action == 'update':
            sessao = Sessao.objects.get(evento=evento, url=sessao_url)
            return update(request, sessao)
    except Sessao.DoesNotExist:
        raise Http404('Sessão de conteúdo não encontrado')

    context = {
        'objects': sessoes,
        'object': sessao,
        'evento': evento,
        'content_type': CONTENT_TYPE,
        'page_header': page_header,
        'action': action,
    }

    return render(request, template, context)
