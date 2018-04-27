# -*- coding: utf-8 -*-

from django.shortcuts import redirect, render
from django.http import Http404
from django.utils.text import slugify

from caninana.forms.menu_forms import MenuForm
from caninana.models import Menu
from caninana.contents import portal_catalog_content

import datetime

TEMPLATE = 'caninana/comum/%s.html'
CONTENT_TYPE = 'at_menu'

def create(request, evento, **kwargs):
    template = TEMPLATE % 'forms'
    form = MenuForm(request.POST or None, instance=None)
    pai = kwargs.get('pai', None)
    if form.is_valid():
        menu = form.save(commit=False)
        menu.evento = evento
        if pai:
            menu.menu_pai = pai
        #if not form.cleaned_data['url'].strip():
        #    menu.url = slugify(menu.titulo)
        menu.save()
        portal_catalog_content.create(menu, CONTENT_TYPE)
        if pai:
            return redirect('eventweb:index', _evento=pai.evento.url, _content=pai.url)
        return redirect('eventweb:index', _evento=menu.evento.url, _content=menu.url)
    context={
        'form':form,
        'content_type':CONTENT_TYPE,
        'page_header':'Novo Menu',
        'subtext':'',
        'action':'create',
        'evento':evento,
    }
    return render(request, template, context)

def update(request, menu):
    _url = menu.url
    template = TEMPLATE % 'forms'
    form = MenuForm(request.POST or None, instance=menu)
    if form.is_valid():
        menu = form.save(commit=False)
        #if not form.cleaned_data['url'].strip():
        #    menu.url = slugify(menu.titulo)
        menu.save()
        portal_catalog_content.update(menu, _url)
        return redirect('eventweb:index', _evento=menu.evento.url, _content=menu.url)
    context = {
        'object':menu,
        'form': form,
        'content_type': CONTENT_TYPE,
        'page_header': 'Atualizando meno',
        'subtext': '',
        'action': 'update',
        'evento': menu.evento,
    }
    return render(request, template, context)

def view(request, evento, menu_url, listar=False):
    template = TEMPLATE % 'menus'
    action = request.GET.get('action', None)
    createObject = request.GET.get('@@createObject', None)
    menus = None
    menu = None
    page_header = None
    try:
        if createObject:
            menu = Menu.objects.get(evento=evento, url=menu_url)
            return create(request, evento, pai=menu)
        if listar:
            menus = Menu.objects.filter(evento=evento, menu_pai=None)
            page_header = 'Lista de Menus'
        else:
            menu = Menu.objects.get(evento=evento, url=menu_url)
            page_header = menu.titulo
        if action == 'update':
            menu = Menu.objects.get(evento=evento, url=menu_url)
            return update(request, menu)
    except Menu.DoesNotExist:
        raise Http404('Menu de conteúdo não encontrado')

    context = {
        'objects':menus,
        'object':menu,
        'evento':evento,
        'content_type':CONTENT_TYPE,
        'page_header': page_header,
        'action':action,
    }

    return render(request, template, context)