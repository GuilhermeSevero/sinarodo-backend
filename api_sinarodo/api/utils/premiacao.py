from datetime import date, timedelta, datetime
import calendar
from rest_framework import serializers
from django.db.models import Sum
from ..serializers.obras_usuarios import ObrasUsuariosSerializer
from ..serializers.premiacoes import PremiacoesSerializer
from ..models.obras import Obras
from ..models.configuracoes import Configuracoes


class Premiacao:
    def __init__(self, id_obra, categorias, data_incio, data_final, observacao):
        try:
            self.obra = Obras.objects.get(pk=id_obra)
        except Obras.DoesNotExist:
            raise serializers.ValidationError('Obra não encontrada!')

        self.data_inicio = datetime.strptime(data_incio, '%Y-%m-%d').date()
        self.data_final = datetime.strptime(data_final, '%Y-%m-%d').date()

        if (self.data_inicio < self.obra.data_inicio) \
                or (self.obra.data_final and self.data_final > self.obra.data_final):
            raise serializers.ValidationError('Data do lançamento fora do período da obra!')

        self.categorias = categorias
        self.observacao = observacao

    def premiar(self, id_usuario, encarregado=False):
        mes_inicio = int(self.data_inicio.strftime("%m"))
        ano_inicio = int(self.data_inicio.strftime("%Y"))

        mes_fim = int(self.data_final.strftime("%m"))
        ano_fim = int(self.data_final.strftime("%Y"))

        mes_fim += (12 * (ano_fim - ano_inicio))

        data_atual = self.data_inicio
        ano_atual = ano_inicio

        obras_usuario = self._criar_obra_usuario(
            id_usuario=id_usuario,
            encarregado=encarregado
        )

        for i in range(mes_inicio, mes_fim + 1):
            if i > 12:
                mes_atual = 1
                ano_atual += 1
            else:
                mes_atual = i

            if i < mes_fim:
                if i == 12:
                    proxima_data = date(ano_atual + 1, 1, 1)
                else:
                    proxima_data = date(ano_atual, mes_atual + 1, 1)

                ultimo_dia_mes = proxima_data - timedelta(days=1)
                quantidade_dias = (ultimo_dia_mes - data_atual).days
                data_atual = proxima_data
            else:
                quantidade_dias = (self.data_final - data_atual).days

            pode_premiar = self._validar_dias_trabalhados(
                id_usuario=id_usuario,
                mes=mes_atual,
                ano=ano_atual,
                dias=quantidade_dias + 1
            )
            if not pode_premiar:
                raise serializers.ValidationError(
                    'Dias em campo maior que o total de dias do mês!<br> '
                    'Verifique os lançamentos do usuário: {usuario}<br>'
                    'Em {mes}/{ano}'
                    .format(usuario=obras_usuario.usuario.nome, mes=mes_atual, ano=ano_atual)
                )

            self._do_premiar(
                obras_usuario=obras_usuario,
                encarregado=encarregado,
                mes=mes_atual,
                ano=ano_atual,
                quantidade_dias=quantidade_dias + 1
            )

    def _do_premiar(self, obras_usuario, encarregado, mes, ano, quantidade_dias):
        total_pontos = 0

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

    def _criar_obra_usuario(self, id_usuario, encarregado):
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
        except:
            acrescimo = 0
        return pontuacao * ((acrescimo / 100) + 1)

    def _validar_dias_trabalhados(self, id_usuario, mes, ano, dias):
        premiacoes = PremiacoesSerializer.Meta.model.objects.filter(
            obras_usuario__obra__id=self.obra.id,
            obras_usuario__usuario__id=id_usuario,
            mes_periodo=mes,
            ano_periodo=ano
        )\
            .values('categoria')\
            .order_by('categoria')\
            .annotate(total_dias_em_campo=Sum('dias_em_campo'))

        if premiacoes:
            premiacao = premiacoes.first()
            _, dias_no_mes = calendar.monthrange(ano, mes)
            return premiacao.get('total_dias_em_campo', 0) + dias <= dias_no_mes

        return True



