from ..serializers.obras_usuarios import ObrasUsuariosSerializer
from ..serializers.premiacoes import PremiacoesSerializer
from ..models.obras import Obras
from ..models.configuracoes import Configuracoes
from rest_framework import serializers


class Premiacao:
    def __init__(self, id_obra, categorias, observacao):
        try:
            self.obra = Obras.objects.get(pk=id_obra)
        except Obras.DoesNotExist:
            raise serializers.ValidationError('Obra não encontrada!')
        self.categorias = categorias
        self.observacao = observacao

    def premiar(self, id_usuario, encarregado=False):
        total_pontos = 0

        mes = self.obra.data_inicio.strftime("%m")
        ano = self.obra.data_final.strftime("%Y")
        quantidade_dias = (self.obra.data_final - self.obra.data_inicio).days

        obras_usuario = self._criar_obra_usuario(
            id_usuario=id_usuario,
            encarregado=encarregado
        )

        for categoria in self.categorias:
            total_pontos += self._calcula_pontos(categoria=categoria, encarregado=encarregado)

            self._criar_premiacao(
                id_obras_usuario=obras_usuario.id,
                mes=mes,
                ano=ano,
                dias=quantidade_dias,
                categoria=categoria
            )

        self._atualizar_nota_obras_usuario(
            obras_usuario=obras_usuario,
            nota_final=total_pontos
        )

    def _criar_obra_usuario(self, id_usuario, encarregado=False):
        obras_usuario = ObrasUsuariosSerializer(
            data={
                'id_obra': self.obra.id,
                'id_usuario': id_usuario,
                'nota_final': 0,
                'observacao': self.observacao,
                'encarregado': encarregado
            }
        )
        obras_usuario.is_valid(raise_exception=True)
        obras_usuario.save()
        return obras_usuario.instance

    def _atualizar_nota_obras_usuario(self, obras_usuario, nota_final):
        serializer = ObrasUsuariosSerializer(
            obras_usuario,
            data={
                'nota_final': nota_final
            },
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

    def _criar_premiacao(self, id_obras_usuario, mes, ano, dias, categoria):
        premiacao = PremiacoesSerializer(
            None,
            data={
                'mes_periodo': mes,
                'ano_periodo': ano,
                'dias_em_campo': dias,
                'id_obras_usuario': id_obras_usuario,
                'id_categoria': categoria.get('id'),
                'nota': categoria.get('nota', 0)
            }
        )
        premiacao.is_valid(raise_exception=True)
        premiacao.save()
        return premiacao.instance

    def _calcula_pontos(self, categoria, encarregado):
        pontuacao = categoria.get('nota', 0) * (categoria.get('peso', 0) / 100)
        if encarregado:
            return self._calcula_acrescimo_encarregado(pontuacao)
        return pontuacao

    @staticmethod
    def _calcula_acrescimo_encarregado(pontuacao):
        try:
            acrescimo = Configuracoes.objects.first().acrescimo_encarregado
        except Configuracoes.DoesNotExist:
            acrescimo = 0
        return pontuacao * ((acrescimo / 100) + 1)

