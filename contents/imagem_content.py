# -*- coding: utf-8 -*-

from django.shortcuts import redirect, render
from django.http import Http404
from django.utils.text import slugify

from caninana.forms.imagem_forms import ImagemForm
from caninana.models import Imagem
from caninana.contents import portal_catalog_content

import datetime

TEMPLATE = 'caninana/comum/%s.html'
CONTENT_TYPE = 'at_imagem'

def create(request, evento):
    template = TEMPLATE % 'forms'
    form = ImagemForm(request.POST or None, request.FILES or None, instance=None)
    if form.is_valid():
        imagem = form.save(commit=False)
        imagem.evento = evento
        imagem.imagem = request.FILES.get('imagem', None)
        #if not form.cleaned_data['url'].strip():
        #    imagem.url = slugify(imagem.titulo)
        imagem.save()
        portal_catalog_content.create(imagem, CONTENT_TYPE)
        response = redirect('eventweb:index', _evento=evento.url, _content=imagem.url)
        return response
    context = {
        'form': form,
        'content_type': CONTENT_TYPE,
        'page_header': 'Nova imagem',
        'subtext': '',
        'action': 'create',
        'evento': evento,
    }
    return render(request, template, context)

def update(request, imagem):
    template = TEMPLATE % 'forms'
    _url = imagem.url
    form = ImagemForm(request.POST or None, request.FILES or None, instance=imagem)
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
        'content_type': CONTENT_TYPE,
        'page_header': 'Atualizando imagem',
        'subtext': '',
        'action':'update',
        'evento':imagem.evento,
        'object':imagem,
    }
    return render(request, template, context)

def view(request, evento, imagem_url):
    template = TEMPLATE % 'imagems'
    fluxo = request.GET.get('workflow', None)
    action = request.GET.get('action', None)
    try:
        imagem = Imagem.objects.get(evento=evento, url=imagem_url)
        if fluxo in ['publicado', 'retirado', 'privado']:
            return workflow(request, evento, imagem, fluxo)
        if action == 'update':
            return update(request, imagem)
    except Imagem.DoesNotExist:
        raise Http404('Informe não encontrado')

    context = {
        'object':imagem,
        'evento':evento,
        'content_type':'at_banner',
        'workflow':imagem.get_fluxo_trabalho_display(),
        'page_header':imagem.titulo,
        'action':'view',
    }

    return render(request, template, context)

def workflow(request, evento, imagem, fluxo):
    imagem.fluxo_trabalho = fluxo
    imagem.publicacao_at = datetime.datetime.now()
    imagem.save()
    portal_catalog_content.workflow(imagem)
    return redirect('eventweb:index', _evento=evento.url, _content=imagem.url)