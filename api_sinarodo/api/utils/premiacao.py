from ..serializers.obras_usuarios import ObrasUsuariosSerializer
from ..serializers.premiacoes import PremiacoesSerializer


class Premiacao:
    def __init__(self, obra, id_usuario, categorias):
        self.obra = obra
        self.id_usuario = id_usuario
        self.categorias = categorias

    def premiar(self, observacao):
        total_pontos = 0

        mes = self.obra.data_inicio.strftime("%m")
        ano = self.obra.data_final.strftime("%Y")
        quantidade_dias = (self.obra.data_final - self.obra.data_inicio).days

        obras_usuario = self._criar_obra_usuario(observacao=observacao)

        for categoria in self.categorias:
            total_pontos += categoria.get('nota') * (categoria.get('peso') / 100)
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

    def _criar_obra_usuario(self, observacao):
        obras_usuario = ObrasUsuariosSerializer(
            data={
                'id_obra': self.obra.id,
                'id_usuario': self.id_usuario,
                'nota_final': 0,
                'observacao': observacao
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
                'nota': categoria.get('nota')
            }
        )
        premiacao.is_valid(raise_exception=True)
        premiacao.save()
        return premiacao.instance
