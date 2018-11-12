from .views import usuarios, categorias, configuracoes, obras, obras_usuarios, premiacoes
from rest_framework.routers import SimpleRouter
from django.conf.urls import url, include


router = SimpleRouter()
router.register('categorias', categorias.CategoriasView, base_name='categorias')
router.register('configuracoes', configuracoes.CategoriasView, base_name='configuracoes')
router.register('obras', obras.ObrasView, base_name='obras')
router.register('usuario_obra', obras_usuarios.ObrasUsuariosView, base_name='usuario_obra')
router.register('premiacoes', premiacoes.PremiacoesView, base_name='premiacoes')
router.register('usuarios', usuarios.UsuariosView, base_name='usuarios')

urlpatterns = [
    url(r'^', include(router.urls)),
]
