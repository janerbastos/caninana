# -*- coding: utf-8 -*-

from django import template
from django.db.models import Q
from django.utils.html import format_html
from django.template.loader import render_to_string

from caninana.models import ESCOLHA_TIPO_CONTEUDO_ICONE
from caninana.processadores import get_content_by_type


register = template.Library()

@register.assignment_tag()
def has_bulder_menu(menus, nivel=0, **kwargs):
    page = ''
    sistema = kwargs.get('sistema', False)
    for menu in menus:
        if not sistema:
            if menu.sub_menus.count > 0:
                context = {
                    'menu':menu,
                    'nivel':nivel,
                }
                page += render_to_string('caninana/comum/templates_tags/builder_menu.html', context)
            else:
                context = {
                    'menu':menu.sub_menus.all(),
                    'nivel':nivel,
                }
                page += render_to_string('caninana/comum/templates_tags/builder_menu.html', context)
        else:

            if menu.sub_menus.count > 0:
                context = {
                    'menu':menu,
                    'nivel':nivel,
                }
                page += render_to_string('caninana/comum/templates_tags/tree_menu_sistema.html', context)
            else:
                context = {
                    'menu':menu.sub_menus.all(),
                    'nivel':nivel,
                }
                page += render_to_string('caninana/comum/templates_tags/tree_menu_sistema.html', context)

    return format_html(page)

@register.inclusion_tag('caninana/tags/menu.html', takes_context=True)
def has_menu(context, **kwargs):
    from caninana.models import Menu
    user = context.request.user
    evento = kwargs.get('evento', None)
    menus = Menu.objects.select_related().filter(evento=evento, menu_pai=None, status=True)
    context = {
        'evento':evento,
        'user':user,
        'menus':menus,
    }
    return context

@register.assignment_tag()
def has_content_menu(tipo, url_evento):
    _html = '<li><a href="%s?%s">%s</i>&nbsp;%s</a></li>'
    item = ESCOLHA_TIPO_CONTEUDO_ICONE[tipo]
    _tag = _html % (url_evento, '@@createObject='+tipo, item[1], item[0])
    return format_html(_tag)

@register.assignment_tag()
def has_contents_by_organizador(organizador, **kwargs):

    from caninana.models import Informe, Link, Pagina

    content_type = organizador.content_type
    categoria = kwargs.get('categoria', 'publico')
    evento = organizador.evento

    if content_type == 'at_informe':
        results = Informe.objects.filter(evento=evento, categoria=categoria, organizador=organizador)

    if content_type == 'at_link':
        results = Link.objects.filter(evento=evento, categoria=categoria, organizador=organizador)

    if content_type == 'at_pagina':
        results = Pagina.objects.filter(evento=evento, categoria=categoria, organizador=organizador)

    context = {'objects': results, 'content_type': content_type}
    page = render_to_string('caninana/comum/templates_tags/list_result_organizadores.html', context)

    return format_html(page)

@register.assignment_tag()
def has_lista_all_contents(objects, **kwargs):
    page = ''
    template = 'caninana/comum/templates_tags/containers.html'
    evento = kwargs.get('evento', None)
    for i in objects:
        page += render_to_string(template, get_content_by_type(i, evento=evento))
    return format_html(page)