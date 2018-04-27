# -*- coding: utf-8 -*-

from django.http import Http404
from .models import ESCOLHA_TIPO_CONTEUDO_ICONE, PortalCatalog, Pagina, Menu, Agenda, Informe, Imagem, Banner,\
    Link, Organizador, Sessao

def get_content_type(evento, content_url):
    """
    Função que retorna o tipo de conteúdo,
    faz a busaca na classe de modelo de catalago de conteúdo
    :param evento: instancia da classe de modelo de evento
    :param content_url: string de url do content
    :return: string do tipo de conteúdo (at_pagina, at_informe, at_agenda, at_link, at_bannaer, at_imagem)
             ou um errro de página não encontrada caso não exista um conteúdo no catalogo
    """
    try:
        pc = PortalCatalog.objects.get(evento=evento, url=content_url)
        return pc.content_type
    except PortalCatalog.DoesNotExist:
        raise Http404('Página não encontrada')

def get_content_by_type(content_type, **kwargs):
    evento = kwargs.get('evento', None)
    content_name = ''
    objects = None
    if content_type == 'at_pagina':
        objects = Pagina.objects.filter(evento=evento)
        content_name = 'Páginas.'

    if content_type == 'at_menu':
        objects = Menu.objects.filter(evento=evento, menu_pai=None)
        content_name = 'Menus.'

    if content_type == 'at_agenda':
        objects = Agenda.objects.filter(evento=evento)
        content_name = 'Agendas.'

    if content_type == 'at_banner':
        objects = Banner.objects.filter(evento=evento)
        content_name = 'Banners.'

    if content_type == 'at_imagem':
        objects = Imagem.objects.filter(evento=evento)
        content_name = 'Imagens.'

    if content_type == 'at_link':
        objects = Link.objects.filter(evento=evento)
        content_name = 'Links.'

    if content_type == 'at_informe':
        objects = Informe.objects.filter(evento=evento)
        content_name = 'Informes.'

    if content_type == 'at_organizador':
        objects = Organizador.objects.filter(evento=evento)
        content_name = 'Organizadores.'

    if content_type == 'at_sessao':
        objects = Sessao.objects.filter(evento=evento)
        content_name = 'Sessões.'

    return {'objects': objects, 'content_name': content_name, 'content_type': content_type, 'icone':ESCOLHA_TIPO_CONTEUDO_ICONE[content_type][1]}