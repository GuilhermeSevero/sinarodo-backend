from django.db import models
from .obras import Obras
from .usuarios import Usuarios
from django.db import connections


class ObrasUsuarios(models.Model):
    class Meta:
        db_table = 'obrasusuarios'
        ordering = ['id']

    obra = models.ForeignKey(Obras, on_delete=models.CASCADE, related_name='usuarios_obra')
    usuario = models.ForeignKey(Usuarios, on_delete=models.PROTECT)
    nota_final = models.FloatField(null=False, blank=False)
    observacao = models.TextField(null=True, blank=True)
    encarregado = models.BooleanField(blank=True, default=False)
    data_inicio = models.DateField(blank=False, null=True)
    data_final = models.DateField(blank=False, null=True)

    @property
    def periodos(self):
        SQL = " SELECT DISTINCT " \
              "	  p.ano_periodo," \
              "   p.mes_periodo," \
              "   p.dias_em_campo" \
              " FROM premiacoes p" \
              " WHERE p.obras_usuario_id = %s" \
              " ORDER BY p.ano_periodo, p.mes_periodo; "

        cursor = connections['default'].cursor()
        cursor.execute(SQL, [self.id])
        premiacoes = cursor.fetchall()
        retorno = []
        for item in premiacoes:
            retorno.append({
                'ano_periodo': item[0],
                'mes_periodo': item[1],
                'dias_em_campo': item[2]
            })
        return retorno
