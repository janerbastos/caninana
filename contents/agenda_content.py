# -*- coding: utf-8 -*-

from django.shortcuts import redirect, render
from django.http import Http404
from django.utils.text import slugify

from caninana.forms.agenda_forms import AgendaForm
from caninana.models import Agenda
from caninana.contents import portal_catalog_content

import datetime

TEMPLATE = 'caninana/comum/%s.html'
CONTENT_TYPE = 'at_agenda'

def create(request, evento):
    template = TEMPLATE % 'forms'
    form = AgendaForm(request.POST or None, instance=None)
    if form.is_valid():
        agenda = form.save(commit=False)
        agenda.evento = evento
        #if not form.cleaned_data['url'].strip():
        #    agenda.url = slugify(agenda.titulo)
        agenda.save()
        portal_catalog_content.create(agenda, CONTENT_TYPE)
        response = redirect('eventweb:index', _evento=evento.url, _content=agenda.url)
        return response
    context={
        'form':form,
        'content_type':CONTENT_TYPE,
        'page_header':'Nova agenda de evento',
        'subtext':'',
        'action':'create',
        'evento':evento,
    }
    return render(request, template, context)

def update(request, agenda):
    template = TEMPLATE % 'forms'
    _url = agenda.url
    form = AgendaForm(request.POST or None, instance=agenda)
    if form.is_valid():
        model = form.save(commit=False)
        model.atualizacao_at = datetime.datetime.now()
        #if not form.cleaned_data['url'].strip():
        #    model.url = slugify(model.titulo)
        model.save()
        portal_catalog_content.update(agenda, _url)
        return redirect('eventweb:index', _evento=model.evento.url, _content=model.url)
    context = {
        'form': form,
        'content_type': CONTENT_TYPE,
        'page_header':'Atualizando agenda',
        'subtext':'',
        'action':'update',
        'evento':agenda.evento,
        'object':agenda,
    }
    return render(request, template, context)

def view(request, evento, agenda_url):
    template = TEMPLATE % 'agendas'
    fluxo = request.GET.get('workflow', None)
    action = request.GET.get('action', None)
    try:
        agenda = Agenda.objects.get(evento=evento, url=agenda_url)
        if fluxo in ['publicado', 'retirado', 'privado']:
            return workflow(request, evento, agenda, fluxo)
        if action == 'update':
            return update(request, agenda)
    except Agenda.DoesNotExist:
        raise Http404('Agenda de evento não encontrada')

    context = {
        'object':agenda,
        'evento':evento,
        'content_type':'at_agenda',
        'workflow':agenda.get_fluxo_trabalho_display(),
        'page_header':agenda.titulo,
        'action':'view',
    }

    return render(request, template, context)

def workflow(request, evento, pagina, fluxo):
    pagina.fluxo_trabalho = fluxo
    pagina.publicacao_at = datetime.datetime.now()
    pagina.save()
    portal_catalog_content.workflow(pagina)
    return redirect('eventweb:index', _evento=evento.url, _content=pagina.url)