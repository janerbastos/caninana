# -*- coding: utf-8 -*-

from django.shortcuts import redirect, render
from django.http import Http404
from django.utils.text import slugify

from caninana.forms.organizador_forms import OrganizadorForm
from caninana.models import Organizador
from caninana.contents import portal_catalog_content

import datetime

TEMPLATE = 'caninana/comum/%s.html'
CONTENT_TYPE = 'at_organizador'

def create(request, evento):
    template = TEMPLATE % 'forms'
    form = OrganizadorForm(request.POST or None, instance=None)
    if form.is_valid():
        organizador = form.save(commit=False)
        organizador.evento = evento
        #if not form.cleaned_data['url'].strip():
        #    organizador.url = slugify(organizador.titulo)
        organizador.save()
        portal_catalog_content.create(organizador, CONTENT_TYPE)
        return redirect('eventweb:index', _evento=organizador.evento.url, _content=organizador.url)
    context={
        'form':form,
        'content_type':CONTENT_TYPE,
        'page_header':'Novo organizador',
        'subtext':'',
        'action':'create',
        'evento':evento,
    }
    return render(request, template, context)

def update(request, organizador):
    template = TEMPLATE % 'forms'
    _url = organizador.url
    form = OrganizadorForm(request.POST or None, instance=organizador)
    if form.is_valid():
        organizador = form.save(commit=False)
        #if not form.cleaned_data['url'].strip():
        #    organizador.url = slugify(organizador.titulo)
        organizador.save()
        portal_catalog_content.update(organizador, _url)
        return redirect('eventweb:index', _evento=organizador.evento.url, _content=organizador.url)
    context = {
        'object':organizador,
        'form': form,
        'content_type': CONTENT_TYPE,
        'page_header': 'Atualizando organizador',
        'subtext': '',
        'action': 'update',
        'evento': organizador.evento,
    }
    return render(request, template, context)

def view(request, evento, organizador_url, listar=False):
    template = TEMPLATE % 'organizadores'
    action = request.GET.get('action', None)
    organizadores = None
    organizador = None
    page_header = None
    try:
        if listar:
            organizadores = Organizador.objects.filter(evento=evento)
            page_header = 'Lista de Organizadores'
        else:
            organizador = Organizador.objects.get(evento=evento, url=organizador_url)
            page_header = organizador.titulo
        if action == 'update':
            organizador = Organizador.objects.get(evento=evento, url=organizador_url)
            return update(request, organizador)
    except Organizador.DoesNotExist:
        raise Http404('Organizador de conteúdo não encontrado')

    context = {
        'objects':organizadores,
        'object':organizador,
        'evento':evento,
        'content_type':CONTENT_TYPE,
        'page_header': page_header,
        'action':action,
    }

    return render(request, template, context)