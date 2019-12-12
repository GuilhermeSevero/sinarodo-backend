from ..models.premiacoes import Premiacoes
from rest_flex_fields import FlexFieldsModelSerializer
from rest_framework import serializers
from .categorias import CategoriasSerializer
from .obras_usuarios import ObrasUsuariosSerializer
from ..models.configuracoes import Configuracoes
from django.db import connections


class PremiacoesSerializer(FlexFieldsModelSerializer):
    id_categoria = serializers.IntegerField(source='categoria_id', required=True)
    id_obras_usuario = serializers.IntegerField(source='obras_usuario_id', required=True)

    class Meta:
        model = Premiacoes
        fields = ('id', 'id_categoria', 'id_obras_usuario', 'mes_periodo', 'ano_periodo', 'dias_em_campo', 'nota')

    expandable_fields = {
        'categoria': (CategoriasSerializer, {'source': 'categoria'}),
        'obras_usuario': (ObrasUsuariosSerializer, {'source': 'obras_usuario'})
    }

    def buscar_dados_mensais(self, mes, ano):
        SQL = ' SELECT ' \
              '	  u.nome,' \
              '   (SUM(ou.nota_final) / COUNT(1)) AS nota_media,' \
              '   SUM(p.dias_em_campo) AS dias_em_campo,' \
              '   u.id,' \
              '   u.matricula,' \
              '   u.funcao_1' \
              ' FROM premiacoes p' \
              ' INNER JOIN obrasusuarios ou' \
              '	  ON p.obras_usuario_id = ou.id' \
              ' INNER JOIN usuarios u' \
              '	  ON ou.usuario_id = u.id' \
              ' WHERE p.categoria_id = (SELECT c.id FROM categorias c LIMIT 1)' \
              '	  AND p.ano_periodo = %s' \
              '   AND p.mes_periodo = %s' \
              ' GROUP BY u.id, u.nome, u.matricula, u.funcao_1 ' \
              ' ORDER BY u.nome; '

        cursor = connections['default'].cursor()
        cursor.execute(SQL, [ano, mes])
        premiacoes = cursor.fetchall()
        retorno = [
            {
                'usuario': {
                    'id': item[3],
                    'matricula': item[4],
                    'nome': item[0],
                    'funcao_1': item[5]
                },
                'nota_media': '{0:.2f}'.format(item[1]),
                'dias_em_campo': item[2],
                'valor_premio': self._premiar(nota_media=item[1], dias_em_campo=item[2])
            } for item in premiacoes
        ]
        return retorno

    def buscar_dados_anual(self, ano):
        SQL = ' SELECT ' \
              '	  u.nome,' \
              '   (SUM(ou.nota_final) / COUNT(1)) AS nota_media,' \
              '   SUM(p.dias_em_campo) AS dias_em_campo,' \
              '   u.id,' \
              '   u.matricula,' \
              '   u.funcao_1' \
              ' FROM premiacoes p' \
              ' INNER JOIN obrasusuarios ou' \
              '	  ON p.obras_usuario_id = ou.id' \
              ' INNER JOIN usuarios u' \
              '	  ON ou.usuario_id = u.id' \
              ' WHERE p.categoria_id = (SELECT c.id FROM categorias c LIMIT 1)' \
              '	  AND p.ano_periodo = %s' \
              ' GROUP BY u.id, u.nome, u.matricula, u.funcao_1 ' \
              ' ORDER BY u.nome; '

        cursor = connections['default'].cursor()
        cursor.execute(SQL, [ano])
        premiacoes = cursor.fetchall()
        relatorio_final = [
            {
                'usuario': {
                    'id': item[3],
                    'matricula': item[4],
                    'nome': item[0],
                    'funcao_1': item[5]
                },
                'nota_media': '{0:.2f}'.format(item[1]),
                'dias_em_campo': item[2],
                'valor_premio': 0.0
            } for item in premiacoes
        ]

        for mes in range(1, 13):
            premios_do_mes = self.buscar_dados_mensais(mes=mes, ano=ano)
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
        return relatorio_final

    def buscar_dados_usuario(self, ano, mes, usuario):
        SQL = ' SELECT ' \
              '   (SUM(ou.nota_final) / COUNT(1)) AS nota_media,' \
              '	  SUM(p.dias_em_campo) AS dias_em_campo ' \
              ' FROM premiacoes p ' \
              ' INNER JOIN obrasusuarios ou' \
              '	  ON p.obras_usuario_id = ou.id ' \
              ' WHERE p.categoria_id = (SELECT c.id FROM categorias c LIMIT 1) ' \
              '	  AND p.ano_periodo = %s ' \
              '   AND' \
              ' p.mes_periodo = %s ' \
              '   AND ou.usuario_id = %s;'

        cursor = connections['default'].cursor()
        cursor.execute(SQL, [ano, mes, usuario])
        premiacoes = cursor.fetchone()
        if premiacoes[0]:
            return {
                'nota_media': '{0:.2f}'.format(premiacoes[0]),
                'dias_em_campo': premiacoes[1],
                'valor_premio': self._premiar(nota_media=premiacoes[0], dias_em_campo=premiacoes[1])
            }
        return {}

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
