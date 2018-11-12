# Generated by Django 2.1.3 on 2018-11-11 22:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categorias',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.CharField(max_length=100, unique=True)),
                ('peso', models.IntegerField()),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Configuracoes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valor_por_ponto', models.FloatField()),
                ('acrescimo_encarregado', models.FloatField()),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Obras',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pedido', models.IntegerField(unique=True)),
                ('data_lancamento', models.DateField()),
                ('data_inicio', models.DateField()),
                ('data_final', models.DateField(blank=True, null=True)),
                ('observacao', models.TextField(blank=True, null=True)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='ObrasUsuarios',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nota_final', models.IntegerField()),
                ('observacao', models.TextField(blank=True, null=True)),
                ('obra', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Obras')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Premiacoes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mes_periodo', models.IntegerField()),
                ('ano_periodo', models.IntegerField()),
                ('dias_em_campo', models.IntegerField()),
                ('nota', models.IntegerField()),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='api.Categorias')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Usuarios',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('matricula', models.IntegerField(blank=True, null=True, unique=True)),
                ('nome', models.CharField(max_length=255)),
                ('apelido', models.CharField(blank=True, max_length=60, null=True)),
                ('cpf', models.CharField(blank=True, max_length=11, null=True, unique=True)),
                ('email', models.CharField(blank=True, max_length=255, null=True)),
                ('telefone', models.CharField(blank=True, max_length=11, null=True)),
                ('login', models.CharField(max_length=30, unique=True)),
                ('password', models.CharField(max_length=255)),
                ('precisa_novo_password', models.BooleanField(blank=True, default=True)),
                ('permissao', models.IntegerField(blank=True, default=3)),
                ('funcao_1', models.CharField(blank=True, max_length=30, null=True)),
                ('funcao_2', models.CharField(blank=True, max_length=30, null=True)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.AddField(
            model_name='obrasusuarios',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='api.Usuarios'),
        ),
    ]