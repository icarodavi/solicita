# Generated by Django 4.0.3 on 2022-04-03 17:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('produto', '0005_produto_unidade'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='produto',
            name='slug',
        ),
    ]
