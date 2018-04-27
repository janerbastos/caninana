# -*- coding: utf-8 -*-

from django.shortcuts import redirect, render
from django.http import Http404
from django.utils.text import slugify

from caninana.forms.banner_forms import BannerForm
from caninana.models import Banner
from caninana.contents import portal_catalog_content

import datetime

TEMPLATE = 'caninana/comum/%s.html'
CONTENT_TYPE = 'at_banner'

def create(request, evento):
    template = TEMPLATE % 'forms'
    form = BannerForm(request.POST or None, request.FILES or None, instance=None)
    if form.is_valid():
        banner = form.save(commit=False)
        banner.evento = evento
        banner.imagem = request.FILES.get('imagem', None)
        #if not form.cleaned_data['url'].strip():
        #    banner.url = slugify(banner.titulo)
        banner.save()
        portal_catalog_content.create(banner, CONTENT_TYPE)
        response = redirect('eventweb:index', _evento=evento.url, _content=banner.url)
        return response
    context = {
        'form': form,
        'content_type': CONTENT_TYPE,
        'page_header': 'Novo banner',
        'subtext': '',
        'action': 'create',
        'evento': evento,
    }
    return render(request, template, context)

def update(request, banner):
    template = TEMPLATE % 'forms'
    _url = banner.url
    form = BannerForm(request.POST or None, request.FILES or None, instance=banner)
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
        'page_header': 'Atualizando banner',
        'subtext': '',
        'action': 'update',
        'evento': banner.evento,
        'object': banner
    }
    return render(request, template, context)

def view(request, evento, banner_url):
    template = TEMPLATE % 'banners'
    fluxo = request.GET.get('workflow', None)
    action = request.GET.get('action', None)
    try:
        banner = Banner.objects.get(evento=evento, url=banner_url)
        if fluxo in ['publicado', 'retirado', 'privado']:
            return workflow(request, evento, banner, fluxo)
        if action == 'update':
            return update(request, banner)
    except Banner.DoesNotExist:
        raise Http404('Informe não encontrado')

    context = {
        'object':banner,
        'evento':evento,
        'content_type':'at_banner',
        'workflow':banner.get_fluxo_trabalho_display(),
        'page_header':banner.titulo,
        'action':'view',
    }

    return render(request, template, context)

def workflow(request, evento, banner, fluxo):
    banner.fluxo_trabalho = fluxo
    banner.publicacao_at = datetime.datetime.now()
    banner.save()
    portal_catalog_content.workflow(banner)
    return redirect('eventweb:index', _evento=evento.url, _content=banner.url)