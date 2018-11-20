from rest_framework import serializers
from ..serializers.obras_usuarios import ObrasUsuariosSerializer
import calendar


class Premiacao:
    def __init__(self, obra, usuario, categorias):
        self.obra = obra
        self.usuario = usuario
        self.categorias = categorias

    def premiar(self):
        total_pontos = 0

        mes_inicio = self.obra.data_inicio.strftime("%m")
        mes_final = self.obra.data_final.strftime("%m")
        meses = 1

        if mes_inicio != mes_final:
            if mes_final < mes_inicio:
                mes_final += 12
            meses = (mes_final - mes_inicio) + 1

        for i in range(meses):



        obras_usuario = self._criar_obra_usuario()
        for categoria in self.categorias:



    def _criar_obra_usuario(self):
        obras_usuario = ObrasUsuariosSerializer(
            data={
                'id_obra': self.obra.id,
                'id_usuario': self.usuario.id
            }
        )
        obras_usuario.is_valid(raise_exception=True)
        obras_usuario.save()
        return obras_usuario
