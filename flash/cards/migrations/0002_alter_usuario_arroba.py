# Generated by Django 5.0.1 on 2024-02-11 23:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='arroba',
            field=models.TextField(unique=True),
        ),
    ]
