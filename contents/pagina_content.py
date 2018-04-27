# -*- coding: utf-8 -*-

from django.shortcuts import redirect, render
from django.http import Http404
from django.utils.text import slugify

from caninana.forms.pagina_form import PaginaForm
from caninana.models import Pagina
from caninana.contents import portal_catalog_content

import datetime

TEMPLATE = 'caninana/comum/%s.html'
CONTENT_TYPE = 'at_pagina'

def create(request, evento):
    template = TEMPLATE % 'forms'
    form = PaginaForm(request.POST or None, instance=None)
    if form.is_valid():
        pagina = form.save(commit=False)
        #if not form.cleaned_data['url'].strip():
        #    pagina.url = slugify(pagina.titulo)
        pagina.evento = evento
        pagina.save()
        portal_catalog_content.create(pagina, CONTENT_TYPE)
        response = redirect('eventweb:index', _evento=evento.url, _content=pagina.url)
        return response
    context={
        'form':form,
        'content_type':CONTENT_TYPE,
        'page_header':'Nova página',
        'subtext':'',
        'action':'create',
        'evento':evento,
    }
    return render(request, template, context)

def update(request, pagina):
    template = TEMPLATE % 'forms'
    _url = pagina.url
    form = PaginaForm(request.POST or None, instance=pagina)
    if form.is_valid():
        model = form.save(commit=False)
        #if not form.cleaned_data['url'].strip():
        #    model.url = slugify(model.titulo)
        model.atualizacao_at = datetime.datetime.now()
        model.save()
        portal_catalog_content.update(model, _url)
        return redirect('eventweb:index', _evento=model.evento.url, _content=model.url)
    context = {
        'form': form,
        'content_type':CONTENT_TYPE,
        'page_header':'Atualizando página',
        'subtext':'',
        'action':'update',
        'evento':pagina.evento,
        'object':pagina,
    }
    return render(request, template, context)

def view(request, evento, pagina_url):
    template = TEMPLATE % 'paginas'
    fluxo = request.GET.get('workflow', None)
    action = request.GET.get('action', None)
    try:
        pagina = Pagina.objects.get(evento=evento, url=pagina_url)
        if fluxo in ['publicado', 'retirado', 'privado']:
            return workflow(request, evento, pagina, fluxo)
        if action == 'update':
            return update(request, pagina)
    except Pagina.DoesNotExist:
        raise Http404('Página não encontrada')

    context = {
        'object':pagina,
        'evento':evento,
        'content_type':'at_pagina',
        'workflow':pagina.get_fluxo_trabalho_display(),
        'page_header':pagina.titulo,
        'action':'view',
    }

    return render(request, template, context)

def workflow(request, evento, pagina, fluxo):
    pagina.fluxo_trabalho = fluxo
    pagina.publicacao_at = datetime.datetime.now()
    pagina.save()
    portal_catalog_content.workflow(pagina)
    return redirect('eventweb:index', _evento=evento.url, _content=pagina.url)