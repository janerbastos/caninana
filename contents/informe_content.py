# -*- coding: utf-8 -*-

from django.shortcuts import redirect, render
from django.http import Http404
from django.utils.text import slugify

from caninana.forms.informe_forms import InformeForm
from caninana.models import Informe
from caninana.contents import portal_catalog_content

import datetime

TEMPLATE = 'caninana/comum/%s.html'
CONTENT_TYPE = 'at_informe'

def create(request, evento):
    template = TEMPLATE % 'forms'
    form = InformeForm(request.POST or None, request.FILES or None, instance=None)
    if form.is_valid():
        informe = form.save(commit=False)
        informe.evento = evento
        informe.imagem = request.FILES.get('imagem', None)
        #if not form.cleaned_data['url'].strip():
        #    informe.url = slugify(informe.titulo)
        informe.save()
        portal_catalog_content.create(informe, CONTENT_TYPE)
        response = redirect('eventweb:index', _evento=evento.url, _content=informe.url)
        return response
    context = {
        'form': form,
        'content_type': CONTENT_TYPE,
        'page_header': 'Novo Informe',
        'subtext': '',
        'action': 'create',
        'evento': evento,
    }
    return render(request, template, context)

def update(request, informe):
    template = TEMPLATE % 'forms'
    _url = informe.url
    form = InformeForm(request.POST or None, request.FILES or None, instance=informe)
    if form.is_valid():
        model = form.save(commit=False)
        model.atualizacao_at = datetime.datetime.now()
        if request.FILES:
            model.imagem = request.FILES.get('imagem', None)
        #if not form.cleaned_data['url'].strip():
        #    model.url = slugify(model.titulo)
        model.save()
        portal_catalog_content.update(model, _url)
        return redirect('eventweb:index', _evento=model.evento.url, _content=model.url)
    context = {
        'form': form,
        'content_type':CONTENT_TYPE,
        'page_header':'Atualizando informe',
        'subtext':'',
        'action':'update',
        'evento':informe.evento,
        'object':informe,
    }
    return render(request, template, context)

def view(request, evento, pagina_url):
    template = TEMPLATE % 'informes'
    fluxo = request.GET.get('workflow', None)
    action = request.GET.get('action', None)
    try:
        informe = Informe.objects.get(evento=evento, url=pagina_url)
        if fluxo in ['publicado', 'retirado', 'privado']:
            return workflow(request, evento, informe, fluxo)
        if action == 'update':
            return update(request, informe)
    except Informe.DoesNotExist:
        raise Http404('Informe não encontrado')

    context = {
        'object':informe,
        'evento':evento,
        'content_type':'at_pagina',
        'workflow':informe.get_fluxo_trabalho_display(),
        'page_header':informe.titulo,
        'action':'view',
    }

    return render(request, template, context)

def workflow(request, evento, informe, fluxo):
    informe.fluxo_trabalho = fluxo
    informe.publicacao_at = datetime.datetime.now()
    informe.save()
    portal_catalog_content.workflow(informe)
    return redirect('eventweb:index', _evento=evento.url, _content=informe.url)