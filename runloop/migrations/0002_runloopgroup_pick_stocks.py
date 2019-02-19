# Generated by Django 2.1.5 on 2019-02-17 06:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pickstock', '0004_pickstockntoppickstock'),
        ('runloop', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='runloopgroup',
            name='pick_stocks',
            field=models.ManyToManyField(related_name='pick_stock_groups', to='pickstock.PickStock', verbose_name='选股因子'),
        ),
    ]
