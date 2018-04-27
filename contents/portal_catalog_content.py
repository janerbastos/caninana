# -*- coding: utf-8 -*-

from django.shortcuts import redirect, render
from django.http import Http404

from caninana.forms.pagina_form import PaginaForm
from caninana.models import PortalCatalog, Organizador, Menu, Sessao

import datetime


def create(content, _type):
    pc = PortalCatalog()
    pc.url = content.url
    pc.titulo = content.titulo
    pc.content_type = _type
    pc.evento = content.evento
    if not isinstance(content, (Organizador, Menu, Sessao)):
        pc.descricao = content.descricao
        pc.categoria = content.categoria
    elif isinstance(content, Sessao):
        pc.descricao = content.descricao
    pc.save()


def update(content, url):
    pc = PortalCatalog.objects.get(evento=content.evento, url=url)
    pc.url = content.url
    pc.titulo = content.titulo
    if isinstance(content, (Organizador, Menu, Sessao)):
        pc.atualizacao_at = datetime.datetime.now()
    elif isinstance(content, Sessao):
        pc.descricao = content.descricao
    else:
        pc.descricao = content.descricao
        pc.atualizacao_at = content.atualizacao_at
        pc.categoria = content.categoria
    pc.save()


def workflow(content):
    pc = PortalCatalog.objects.get(evento=content.evento, url=content.url)
    pc.fluxo_trabalho = content.fluxo_trabalho
    pc.publicacao_at = content.publicacao_at
    pc.save()


def list_content(evento, content_type=None):
    pc = PortalCatalog.objects.filter(evento=evento)
    if content_type:
        pc = pc.filter(content_type=content_type)
    return pc