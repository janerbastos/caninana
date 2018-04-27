# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404

from .models import Evento
from caninana_admin.views import action as manage_event

from caninana_admin.utils import get_evento_request, get_url_request, LIST_KEY_SISTEM
from .contents import pagina_content, informe_content, agenda_content, link_content, banner_content, \
    imagem_content, organizador_content, menu_content, sessao_content, all_contents, item_sessao_content
from .processadores import get_content_type


# Create your views here.

def __despachante__(request, evento, _content, content_type, **kwargs):
    """
    Função despachante, processadora de tipos de conteúdo
    :param request: objeto de requisição
    :param evento: instancia da classe de evento
    :param _content: string da url do content
    :param content_type: string do tipo de conteúdo
    :return: objeto response
    """

    if content_type == 'at_pagina':
        return pagina_content.view(request, evento, _content)

    if content_type == 'at_informe':
        return informe_content.view(request, evento, _content)

    if content_type == 'at_agenda':
        return agenda_content.view(request, evento, _content)

    if content_type == 'at_link':
        return link_content.view(request, evento, _content)

    if content_type == 'at_banner':
        return banner_content.view(request, evento, _content)

    if content_type == 'at_imagem':
        return imagem_content.view(request, evento, _content)

    if content_type == 'at_organizador':
        return organizador_content.view(request, evento, _content, kwargs.get('listar', False))

    if content_type == 'at_menu':
        return menu_content.view(request, evento, _content, kwargs.get('listar', False))

    if content_type == 'at_sessao':
        return sessao_content.view(request, evento, _content, kwargs.get('listar', False))

    if content_type == 'at_item_sessao':
        return item_sessao_content.view(request, evento, _content, kwargs.get('action', None))

    if content_type == 'at_all':
        return all_contents.view(request, evento)

    raise Http404('Tipo de conteudo não encontrado')


def __buider_contents__(request, evento, create_object):
    """
    Função despachande, processadora de criação de contents
    :param request: objeto de requisição web
    :param evento: instancia da classe de evento
    :param create_object: string do tipo de conteúdo a ser criado
    :return: objeto response
    """

    if create_object == 'at_pagina':
        return pagina_content.create(request, evento)

    if create_object == 'at_informe':
        return informe_content.create(request, evento)

    if create_object == 'at_agenda':
        return agenda_content.create(request, evento)

    if create_object == 'at_link':
        return link_content.create(request, evento)

    if create_object == 'at_banner':
        return banner_content.create(request, evento)

    if create_object == 'at_imagem':
        return imagem_content.create(request, evento)

    if create_object == 'at_organizador':
        return organizador_content.create(request, evento)

    if create_object == 'at_menu':
        return menu_content.create(request, evento)

    if create_object == 'at_sessao':
        return sessao_content.create(request, evento)

    raise Http404('Tipo de conteudo não encontrado')


def index(request, _evento, _content=None):
    """
    Função processadorea de requisição
    :param request: objeto de solicitação web
    :param _evento: string da url do evento
    :param _content: string da url do content, parametro opcional
    :return: objeto response da solicitação web
    """

    createObject = request.GET.get('@@createObject', None)
    removeObject = request.GET.get('@@removeObject', None)
    listObject = request.GET.get('@@list', None)
    template = 'caninana/index.html'
    try:
        evento = Evento.objects.get(url=_evento)
    except Evento.DoesNotExist:
        if _evento == 'mana_main':
            return manage_event(request)
        else:
            raise Http404('Evento não encontrado')

    if evento and _content:
        if createObject:
            content_type = createObject
        elif removeObject:
            content_type = removeObject
            return __despachante__(request, evento, _content, content_type, action='remover')
        else:
            content_type = get_content_type(evento, _content)
        return __despachante__(request, evento, _content, content_type)

    if createObject:
        return __buider_contents__(request, evento, createObject)

    if listObject:
        return __despachante__(request, evento, _content, listObject, listar=True)

    context = {
        'evento': evento,
    }

    return render(request, template, context)
