# Generated by Django 4.0.3 on 2022-04-03 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produto', '0006_remove_produto_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='produto',
            name='slug',
            field=models.SlugField(blank=True, null=True),
        ),
    ]
