# Generated by Django 5.0.1 on 2024-02-28 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0009_simulados'),
    ]

    operations = [
        migrations.AddField(
            model_name='simulados',
            name='respostas',
            field=models.TextField(default='a'),
        ),
    ]