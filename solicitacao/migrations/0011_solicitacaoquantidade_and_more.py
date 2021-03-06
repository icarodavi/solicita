# Generated by Django 4.0.3 on 2022-04-05 23:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('solicitacao', '0010_remove_solicitacao_qtd_total'),
    ]

    operations = [
        migrations.CreateModel(
            name='SolicitacaoQuantidade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantidade', models.PositiveIntegerField(default=0)),
            ],
            options={
                'verbose_name': 'Through Quantidade',
                'verbose_name_plural': 'Through Quantidades',
            },
        ),
        migrations.RenameField(
            model_name='solicitacaoitem',
            old_name='quantidade',
            new_name='qtd',
        ),
        migrations.AddField(
            model_name='solicitacaoitem',
            name='soliticao_item',
            field=models.ManyToManyField(related_name='solicitacao', through='solicitacao.SolicitacaoQuantidade', to='solicitacao.solicitacao'),
        ),
        migrations.AddField(
            model_name='solicitacaoquantidade',
            name='item_solicitacao',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quantidade', to='solicitacao.solicitacaoitem'),
        ),
        migrations.AddField(
            model_name='solicitacaoquantidade',
            name='solicitacao',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quantidade', to='solicitacao.solicitacao'),
        ),
    ]
