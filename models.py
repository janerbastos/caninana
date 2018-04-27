# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

# Create your models here.

ESCOLHA_FLUXO_TRABALHO = (
    ('publicado', 'Publicado'),
    ('retirado', 'Retirado'),
    ('privado', 'Privado'),
)

ESCOLHA_CATEGORIA = (
    ('sistema', 'Conteúdo do Sistema.'),
    ('publico', 'Conteúdo público.')
)

ESCOLHA_TARGET = (
    ('_self', 'Abrir o link no mesma janela em que foi clicado (é o padrão)'),
    ('_blank', 'Abrir o link em uma nova janela ou guia'),
    ('_parent', 'Abre o link vinculado no frame pai'),
    ('_top', 'Abre o link no corpo inteiro da janela'),
    ('_framename', 'Abre o link em um frame nomeado'),
)

ESCOLHA_GRUPO = (
    ('administradores', 'Administradores'),
    ('conteudista', 'Conteúdista'),
)

ESCOLHA_TIPO_CONTEUDO = (
    ('at_pagina', 'Página'),
    ('at_informe', 'Informe'),
    ('at_agenda', 'Agenda'),
    ('at_link', 'Link'),
    ('at_banner', 'Banner'),
    ('at_imagem', 'Imagem')
)

ESCOLHA_TIPO_CONTEUDO_ICONE = {
    'at_pagina': ('Pagina', '<i class="fa fa-fw fa-file-text-o"></i>'),
    'at_informe': ('Informe', '<i class="fa fa-fw fa-newspaper-o"></i>'),
    'at_agenda': ('Agenda', '<i class="fa fa-fw fa-calendar"></i>'),
    'at_link': ('Link', '<i class="fa fa-fw fa-link"></i>'),
    'at_banner': ('Banner', '<i class="fa fa-fw fa-image"></i>'),
    'at_imagem': ('Imagem', '<i class="fa fa-fw fa-file-image-o"></i>'),
    'at_organizador': ('Organizador', '<i class="fa fa-fw fa-object-group"></i>'),
    'at_menu': ('Menu', '<i class="fa fa-fw fa-th-list"></i>'),
    'at_sessao': ('Sessao', '<i class="fa fa-fw fa-tv"></i>'),
}


class Sessao(models.Model):
    url = models.SlugField(max_length=200)
    titulo = models.CharField(max_length=100)
    descricao = models.TextField(null=True, blank=True)
    content_type = models.CharField(max_length=20, choices=ESCOLHA_TIPO_CONTEUDO, null=True, blank=True)
    max_contents = models.PositiveIntegerField(default=1)
    evento = models.ForeignKey('Evento')
    contents = models.ManyToManyField('PortalCatalog', through='SessaoContents')
    status = models.BooleanField(default=True)

    class Meta:
        db_table = 'caninana_sessao'

    def __unicode__(self):
        return '%s' % self.titulo

    def get_absolute_url(self):
        return '/%s/%s/' % (self.evento.url, self.url)

    def save(self, **kwargs):
        if not self.url:
            self.url = 'sessao-' + slugify(self.titulo)
        super(Sessao, self).save()


class SessaoContents(models.Model):
    sessao = models.ForeignKey('Sessao')
    portal_catalog = models.ForeignKey('PortalCatalog')

    class Meta:
        db_table = 'caninana_sessao_content'


class Organizador(models.Model):
    url = models.SlugField(max_length=200, unique=True)
    titulo = models.CharField(max_length=50)
    status = models.BooleanField()
    evento = models.ForeignKey('Evento')
    content_type = models.CharField(max_length=20, choices=ESCOLHA_TIPO_CONTEUDO)

    class Meta:
        db_table = 'caninana_organizador'

    def __unicode__(self):
        return self.titulo

    @property
    def get_list_url(self):
        return '/%s/?@@list=%s' % (self.evento.url, 'at_organizador')

    def get_absolute_url(self):
        return '/%s/%s/' % (self.evento.url, self.url)

    def save(self, **kwargs):
        if not self.url:
            self.url = 'organizador-' + slugify(self.titulo)
        super(Organizador, self).save()


class Evento(models.Model):
    url = models.SlugField(max_length=200, unique=True)
    titulo = models.CharField(max_length=100)
    descricao = models.TextField(null=True, blank=True)
    criacao_at = models.DateTimeField(auto_now_add=True)
    publicacao_at = models.DateTimeField(null=True, blank=True)
    atualizacao_at = models.DateTimeField(null=True, blank=True)
    favico = models.ImageField(upload_to='evento/midias', null=True, blank=True)
    logo = models.ImageField(upload_to='evento/midias', null=True, blank=True)
    template = models.CharField(max_length=50, default='default')
    fluxo_trabalho = models.CharField(max_length=20, choices=ESCOLHA_FLUXO_TRABALHO, default='privado')
    inicio_at = models.DateTimeField(null=True, blank=True)
    encerramento_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'caninana_evento'

    def __unicode__(self):
        return self.titulo

    @property
    def edit_evento(self):
        return '/manage_main/?view=%s&action=%s' % (self.url, 'edit')

    @property
    def open_evento(self):
        return '/manage_main/?view=%s' % self.url

    @property
    def novo_evento(self):
        return '/manage_main/?action=%s' % 'new'

    @property
    def view_evento(self):
        return '/manage_main/?view=%s' % self.url

    @property
    def workflow(self):
        return '/manage_main/?view=%s&action=%s' % (self.url, 'fluxo-trabalho')

    @property
    def index_evento(self):
        return '/%s/' % self.url

    def get_absolute_url(self):
        return '/%s/' % self.url

    def save(self, **kwargs):
        if not self.url:
            self.url = slugify(self.titulo)
        super(Evento, self).save()


class Usuario(models.Model):
    evento = models.ForeignKey(Evento, related_name='ref_eventos')
    user = models.ForeignKey(User, related_name="ref_users")
    grupo = models.CharField(max_length=50, choices=ESCOLHA_GRUPO)

    class Meta:
        db_table = 'caninana_usuario'

    def __unicode__(self):
        return self.user.get_full_name()


class Menu(models.Model):
    url = models.SlugField(max_length=200, unique=True)
    titulo = models.CharField(max_length=30)
    link = models.CharField(max_length=255, null=True, blank=True, default='#')
    menu_pai = models.ForeignKey('self', null=True, blank=True, related_name='sub_menus')
    status = models.BooleanField(default=True)
    evento = models.ForeignKey(Evento)

    class Meta:
        db_table = 'caninana_menu'

    def __unicode__(self):
        return self.titulo

    def get_absolute_url(self):
        return '/%s/%s/' % (self.evento.url, self.url)

    def save(self, **kwargs):
        if not self.url:
            self.url = 'menu-' + slugify(self.titulo)
        super(Menu, self).save()


class Content(models.Model):
    url = models.SlugField(max_length=200)
    titulo = models.CharField(max_length=255)
    descricao = models.TextField(null=True, blank=True)
    criacao_at = models.DateTimeField(auto_now_add=True)
    publicacao_at = models.DateTimeField(null=True, blank=True)
    atualizacao_at = models.DateTimeField(null=True, blank=True)
    fluxo_trabalho = models.CharField(max_length=20, choices=ESCOLHA_FLUXO_TRABALHO, default='privado')
    categoria = models.CharField(max_length=20, choices=ESCOLHA_CATEGORIA, default='publico')
    evento = models.ForeignKey(Evento)

    def __unicode__(self):
        return self.titulo

    def get_absolute_url(self):
        return '/%s/%s/' % (self.evento.url, self.url)

    class Meta:
        db_table = 'caninana_content'
        abstract = True
        unique_together = (("evento", "url"),)


class Pagina(Content):
    corpo = models.TextField(null=True, blank=True)
    organizador = models.ForeignKey(Organizador, null=True, blank=True)

    def save(self, **kwargs):
        if not self.url:
            self.url = slugify(self.titulo)
        super(Pagina, self).save()

    class Meta:
        db_table = 'caninana_pagina'


class Informe(Content):
    corpo = models.TextField(null=True, blank=True)
    imagem = models.ImageField(upload_to='evento/midias/informes', null=True, blank=True)
    organizador = models.ForeignKey(Organizador, null=True, blank=True)

    def save(self, **kwargs):
        if not self.url:
            self.url = slugify(self.titulo)
        super(Informe, self).save()

    class Meta:
        db_table = 'caninana_informe'


class Agenda(Content):
    inicio_at = models.DateTimeField()
    termino_at = models.DateTimeField()
    corpo = models.TextField(null=True, blank=True)
    organizador = models.ForeignKey(Organizador, null=True, blank=True)

    def save(self, **kwargs):
        if not self.url:
            self.url = slugify(self.titulo)
        super(Agenda, self).save()

    class Meta:
        db_table = 'caninana_agenda'


# Tipo de contéudo para midias de links internos e externos
class Link(Content):
    link = models.CharField(max_length=200)
    target = models.CharField(max_length=20, choices=ESCOLHA_TARGET, default='_self')
    organizador = models.ForeignKey(Organizador, null=True, blank=True)

    def save(self, **kwargs):
        if not self.url:
            self.url = slugify(self.titulo)
        super(Link, self).save()

    class Meta:
        db_table = 'caninana_link'


# Tipo de conteúdo para midias de imagens para uso em paginas e outros
class Imagem(Content):
    imagem = models.ImageField(upload_to='imagens')
    organizador = models.ForeignKey(Organizador, null=True, blank=True)

    def save(self, **kwargs):
        if not self.url:
            self.url = slugify(self.titulo)
        super(Imagem, self).save()

    class Meta:
        db_table = 'caninana_imagem'


# Tipo de conteúdo para aprentação em destaque
class Banner(Content):
    imagem = models.ImageField(upload_to='evento/midias/banner')
    link = models.CharField(max_length=200)
    target = models.CharField(max_length=20, choices=ESCOLHA_TARGET, default='_self')
    organizador = models.ForeignKey(Organizador, null=True, blank=True)

    def save(self, **kwargs):
        if not self.url:
            self.url = slugify(self.titulo)
        super(Banner, self).save()

    class Meta:
        db_table = 'caninana_banner'


class PortalCatalog(Content):
    content_type = models.CharField(max_length=20, choices=ESCOLHA_TIPO_CONTEUDO)

    class Meta:
        db_table = 'caninana_portal_catalog'

    @property
    def get_content(self):
        if self.content_type == 'at_pagina':
            return Pagina.objects.get(evento=self.evento, url=self.url)
        if self.content_type == 'at_agenda':
            return Agenda.objects.get(evento=self.evento, url=self.url)
        if self.content_type == 'at_link':
            return Link.objects.get(evento=self.evento, url=self.url)
        if self.content_type == 'at_informe':
            return Informe.objects.get(evento=self.evento, url=self.url)
        if self.content_type == 'at_banner':
            return Banner.objects.get(evento=self.evento, url=self.url)
        if self.content_type == 'at_imagem':
            return Imagem.objects.get(evento=self.evento, url=self.url)
        if self.content_type == 'at_menu':
            return Menu.objects.get(evento=self.evento, url=self.url)
        if self.content_type == 'at_organizador':
            return Organizador.objects.get(evento=self.evento, url=self.url)
        if self.content_type == 'at_sessao':
            return Sessao.objects.get(evento=self.evento, url=self.url)
