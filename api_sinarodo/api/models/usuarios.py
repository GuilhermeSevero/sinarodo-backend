from django.db import models


class Usuarios(models.Model):
    class Meta:
        db_table = 'Usuarios'
        ordering = ['id']

    matricula = models.IntegerField(null=True, blank=True, unique=True)
    nome = models.CharField(max_length=255, null=False, blank=False)
    apelido = models.CharField(max_length=60, null=True, blank=True)
    cpf = models.CharField(max_length=11, null=True, blank=True, unique=True)
    email = models.CharField(max_length=255, null=True, blank=True)
    telefone = models.CharField(max_length=11, null=True, blank=True)
    login = models.CharField(max_length=30, null=False, blank=False, unique=True)
    password = models.CharField(max_length=255, null=False, blank=False)
    precisa_novo_password = models.BooleanField(null=False, blank=True, default=True)
    permissao = models.IntegerField(null=False, blank=True, default=3)
    funcao_1 = models.CharField(max_length=30, null=True, blank=True)
    funcao_2 = models.CharField(max_length=30, null=True, blank=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.cpf == '':
            self.cpf = None
        return super(Usuarios, self).save(force_insert, force_update, using, update_fields)
