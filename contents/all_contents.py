# -*- coding: utf-8 -*-

from django.shortcuts import render

from caninana.models import PortalCatalog

TEMPLATE = 'caninana/comum/%s.html'
CONTENT_TYPE = 'at_all'

def view(request, evento):

    template = TEMPLATE % 'list_all_contens'
    pc = PortalCatalog.objects.filter(evento=evento).values_list('content_type', flat=True).distinct().order_by('content_type')

    context = {
        'objects':pc,
        'object':None,
        'evento':evento,
        'content_type':CONTENT_TYPE,
        'page_header': 'Conteúdos deste site',
        'subtext': ' Listagem de todos os conteúdos cadastrados neste site.',
        'action':'list',
    }

    return render(request, template, context)