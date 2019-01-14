# Generated by Django 2.1.5 on 2019-01-13 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('runloop', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='factorbuy',
            name='class_name',
            field=models.CharField(choices=[('AbuFactorBuyBreak', '海龟买'), ('AbuDoubleMaBuy', '双均线买')], editable=False, max_length=32, verbose_name='策略'),
        ),
        migrations.AlterField(
            model_name='factorsell',
            name='class_name',
            field=models.CharField(choices=[('AbuFactorSellBreak', '海龟卖'), ('AbuDoubleMaSell', '双均线卖')], editable=False, max_length=32, verbose_name='策略'),
        ),
        migrations.AlterField(
            model_name='runloopgroup',
            name='factor_buys',
            field=models.ManyToManyField(related_name='factor_buy_groups', to='runloop.FactorBuy', verbose_name='买策略组合'),
        ),
        migrations.AlterField(
            model_name='runloopgroup',
            name='factor_sells',
            field=models.ManyToManyField(related_name='factor_sell_groups', to='runloop.FactorSell', verbose_name='卖策略组合'),
        ),
        migrations.AlterField(
            model_name='runloopgroup',
            name='status',
            field=models.CharField(blank=True, default='新建', max_length=64, verbose_name='状态'),
        ),
    ]
