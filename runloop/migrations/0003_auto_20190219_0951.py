# Generated by Django 2.1.5 on 2019-02-19 01:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('runloop', '0002_runloopgroup_pick_stocks'),
    ]

    operations = [
        migrations.AlterField(
            model_name='runloopgroup',
            name='pick_stocks',
            field=models.ManyToManyField(blank=True, related_name='pick_stock_groups', to='pickstock.PickStock', verbose_name='选股因子'),
        ),
    ]
