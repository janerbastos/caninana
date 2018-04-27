# -*- coding: utf-8 -*-

from django.shortcuts import redirect, render
from django.http import Http404
from django.utils.text import slugify

from caninana.forms.link_forms import LinkForm
from caninana.models import Link
from caninana.contents import portal_catalog_content

import datetime

TEMPLATE = 'caninana/comum/%s.html'
CONTENT_TYPE = 'at_link'

def create(request, evento):
    template = TEMPLATE % 'forms'
    form = LinkForm(request.POST or None, instance=None)
    if form.is_valid():
        link = form.save(commit=False)
        link.evento = evento
        #if not form.cleaned_data['url'].strip():
        #    link.url = slugify(link.titulo)
        link.save()
        portal_catalog_content.create(link, CONTENT_TYPE)
        response = redirect('eventweb:index', _evento=evento.url, _content=link.url)
        return response
    context={
        'form':form,
        'content_type':CONTENT_TYPE,
        'page_header':'Novo link',
        'subtext':'',
        'action':'create',
        'evento':evento,
    }
    return render(request, template, context)

def update(request, link):
    template = TEMPLATE % 'forms'
    _url = link.url
    form = LinkForm(request.POST or None, instance=link)
    if form.is_valid():
        model = form.save(commit=False)
        model.atualizacao_at = datetime.datetime.now()
        #if not form.cleaned_data['url'].strip():
        #    model.url = slugify(model.titulo)
        model.save()
        portal_catalog_content.update(model, _url)
        return redirect('eventweb:index', _evento=model.evento.url, _content=model.url)
    context = {
        'form': form,
        'content_type':CONTENT_TYPE,
        'page_header':'Atualizando link',
        'subtext':'',
        'action':'update',
        'evento':link.evento,
        'object':link,
    }
    return render(request, template, context)

def view(request, evento, link_url):
    template = TEMPLATE % 'links'
    fluxo = request.GET.get('workflow', None)
    action = request.GET.get('action', None)
    try:
        link = Link.objects.get(evento=evento, url=link_url)
        if fluxo in ['publicado', 'retirado', 'privado']:
            return workflow(request, evento, link, fluxo)
        if action == 'update':
            return update(request, link)
    except Link.DoesNotExist:
        raise Http404('Página não encontrada')

    context = {
        'object':link,
        'evento':evento,
        'content_type':'at_link',
        'workflow':link.get_fluxo_trabalho_display(),
        'page_header':link.titulo,
        'action':'view',
    }

    return render(request, template, context)

def workflow(request, evento, link, fluxo):
    link.fluxo_trabalho = fluxo
    link.publicacao_at = datetime.datetime.now()
    link.save()
    portal_catalog_content.workflow(link)
    return redirect('eventweb:index', _evento=evento.url, _content=link.url)