# Generated by Django 5.0.1 on 2024-02-17 23:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0004_remove_pagina_pergunta_remove_pagina_resposta_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='tipo_user',
            field=models.CharField(choices=[('professor', 'Professor'), ('aluno', 'Aluno')], max_length=10),
        ),
    ]
