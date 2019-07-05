from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import FilterSet, DjangoFilterBackend
from rest_flex_fields.views import FlexFieldsMixin
from django_filters import NumberFilter, BooleanFilter
from rest_framework import serializers
from django.db import connections
from rest_framework.response import Response
from ..serializers.premiacoes import Premiacoes, PremiacoesSerializer
from ..models.configuracoes import Configuracoes


class PremiacoesFilterSet(FilterSet):
    id_categoria = NumberFilter(field_name='categoria__id')
    pedido = NumberFilter(field_name='obras_usuario__obra__pedido')
    id_usuario_obra = NumberFilter(field_name='obras_usuario__id')

    class Meta:
        model = Premiacoes
        fields = ('id', 'mes_periodo', 'ano_periodo', 'dias_em_campo', 'nota')


class PremiacoesView(FlexFieldsMixin, ModelViewSet):
    serializer_class = PremiacoesSerializer
    queryset = Premiacoes.objects.all()
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_class = PremiacoesFilterSet
    ordering_fields = (
        'id',
        'ano_periodo',
        'mes_periodo',
        'obras_usuario__usuario__nome',
        'categoria__descricao'
    )

    permit_list_expands = [
        'categoria',
        'obras_usuario',
        'obras_usuario.obra',
        'obras_usuario.usuario'
    ]

    @action(methods=["GET"], detail=False)
    def relatorio_mensal(self, request, *args, **kwargs):
        mes = request.query_params.get('mes', None)
        ano = request.query_params.get('ano', None)

        if not (mes and ano):
            raise serializers.ValidationError('Informe o Mês e o Ano para o relatório!')

        return Response(self._buscar_dados_mensais(mes=mes, ano=ano))

    def _buscar_dados_mensais(self, mes, ano):
        SQL = " SELECT " \
              "	  u.nome," \
              "   (SUM(ou.nota_final) / COUNT(1)) AS nota_media," \
              "   SUM(p.dias_em_campo) AS dias_em_campo," \
              "   u.id," \
              "   u.matricula," \
              "   u.funcao_1" \
              " FROM premiacoes p" \
              " INNER JOIN obrasusuarios ou" \
              "	  ON p.obras_usuario_id = ou.id" \
              " INNER JOIN usuarios u" \
              "	  ON ou.usuario_id = u.id" \
              " WHERE p.categoria_id = (SELECT c.id FROM categorias c LIMIT 1)" \
              "	  AND p.ano_periodo = %s" \
              "   AND p.mes_periodo = %s" \
              " GROUP BY u.id, u.nome, u.matricula, u.funcao_1 " \
              " ORDER BY u.nome; "

        cursor = connections['default'].cursor()
        cursor.execute(SQL, [ano, mes])
        premiacoes = cursor.fetchall()
        retorno = []
        for item in premiacoes:
            retorno.append({
                'usuario': {
                    'id': item[3],
                    'matricula': item[4],
                    'nome': item[0],
                    'funcao_1': item[5]
                },
                'nota_media': "{0:.2f}".format(item[1]),
                'dias_em_campo': item[2],
                'valor_premio': self._premiar(nota_media=item[1], dias_em_campo=item[2])
            })
        return retorno

    @action(methods=["GET"], detail=False)
    def relatorio_anual(self, request, *args, **kwargs):
        ano = request.query_params.get('ano', None)

        if not ano:
            raise serializers.ValidationError('Informe o Ano para o relatório!')

        SQL = " SELECT " \
              "	  u.nome," \
              "   (SUM(ou.nota_final) / COUNT(1)) AS nota_media," \
              "   SUM(p.dias_em_campo) AS dias_em_campo," \
              "   u.id," \
              "   u.matricula," \
              "   u.funcao_1" \
              " FROM premiacoes p" \
              " INNER JOIN obrasusuarios ou" \
              "	  ON p.obras_usuario_id = ou.id" \
              " INNER JOIN usuarios u" \
              "	  ON ou.usuario_id = u.id" \
              " WHERE p.categoria_id = (SELECT c.id FROM categorias c LIMIT 1)" \
              "	  AND p.ano_periodo = %s" \
              " GROUP BY u.id, u.nome, u.matricula, u.funcao_1 " \
              " ORDER BY u.nome; "

        cursor = connections['default'].cursor()
        cursor.execute(SQL, [ano])
        premiacoes = cursor.fetchall()
        relatorio_final = []
        for item in premiacoes:
            relatorio_final.append({
                'usuario': {
                    'id': item[3],
                    'matricula': item[4],
                    'nome': item[0],
                    'funcao_1': item[5]
                },
                'nota_media': "{0:.2f}".format(item[1]),
                'dias_em_campo': item[2],
                'valor_premio': 0.0
            })

        for mes in range(1, 13):
            premios_do_mes = self._buscar_dados_mensais(mes=mes, ano=ano)
            for premio in premios_do_mes:
                encontrado = False
                for premio_final in relatorio_final:
                    if premio['usuario']['id'] == premio_final['usuario']['id']:
                        premio_final['dias_em_campo'] += premio['dias_em_campo']
                        premio_final['valor_premio'] += premio['valor_premio']
                        encontrado = True
                        break
                if not encontrado:
                    relatorio_final.append(premio)

        return Response(relatorio_final)

    @action(methods=["GET"], detail=False)
    def relatorio_usuario(self, request, *args, **kwargs):
        mes = request.query_params.get('mes', None)
        ano = request.query_params.get('ano', None)
        usuario = request.query_params.get('usuario', None)

        if not (usuario and mes and ano):
            raise serializers.ValidationError('Informe o Usuário, Mês e o Ano para o relatório!')

        SQL = " SELECT " \
              "   (SUM(ou.nota_final) / COUNT(1)) AS nota_media," \
              "	  SUM(p.dias_em_campo) AS dias_em_campo " \
              " FROM premiacoes p " \
              " INNER JOIN obrasusuarios ou" \
              "	  ON p.obras_usuario_id = ou.id " \
              " WHERE p.categoria_id = (SELECT c.id FROM categorias c LIMIT 1) " \
              "	  AND p.ano_periodo = %s " \
              "   AND p.mes_periodo = %s " \
              "   AND ou.usuario_id = %s;"

        cursor = connections['default'].cursor()
        cursor.execute(SQL, [ano, mes, usuario])
        premiacoes = cursor.fetchone()
        if premiacoes[0]:
            return Response({
                'nota_media': "{0:.2f}".format(premiacoes[0]),
                'dias_em_campo': premiacoes[1],
                'valor_premio': self._premiar(nota_media=premiacoes[0], dias_em_campo=premiacoes[1])
            })
        return Response({})

    @staticmethod
    def _premiar(nota_media, dias_em_campo):
        try:
            config = Configuracoes.objects.first()
            if dias_em_campo >= config.dias_em_campo:
                if nota_media > 10:
                    return config.premio_dez
                opcoes = {
                    6: config.premio_seis,
                    7: config.premio_sete,
                    8: config.premio_oito,
                    9: config.premio_nove,
                    10: config.premio_dez
                }
                return opcoes.get(int(nota_media), 0)
        except Exception:
            pass
        return 0.0
