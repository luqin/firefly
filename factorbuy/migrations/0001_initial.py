# Generated by Django 2.1.4 on 2019-02-01 07:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FactorBuy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='名称')),
                ('factor_name', models.CharField(editable=False, max_length=64, verbose_name='策略名称')),
                ('class_name', models.CharField(editable=False, max_length=256, verbose_name='策略')),
            ],
            options={
                'verbose_name': '买策略',
                'verbose_name_plural': '买策略',
            },
        ),
        migrations.CreateModel(
            name='FactorBuyBreakXd',
            fields=[
                ('factorbuy_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='factorbuy.FactorBuy')),
                ('xd', models.IntegerField(verbose_name='周期')),
            ],
            options={
                'verbose_name': '海龟买入',
                'verbose_name_plural': '海龟买入',
            },
            bases=('factorbuy.factorbuy',),
        ),
        migrations.CreateModel(
            name='FactorBuyDoubleMa',
            fields=[
                ('factorbuy_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='factorbuy.FactorBuy')),
                ('slow_int', models.IntegerField(verbose_name='慢线(-1:为自动)')),
                ('fast_int', models.IntegerField(verbose_name='快线(-1:为自动)')),
            ],
            options={
                'verbose_name': '双均线买',
                'verbose_name_plural': '双均线买',
            },
            bases=('factorbuy.factorbuy',),
        ),
        migrations.CreateModel(
            name='FactorBuySDBreak',
            fields=[
                ('factorbuybreakxd_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='factorbuy.FactorBuyBreakXd')),
                ('poly', models.IntegerField(verbose_name='拟合')),
            ],
            options={
                'verbose_name': '平稳突破买',
                'verbose_name_plural': '平稳突破买',
            },
            bases=('factorbuy.factorbuybreakxd',),
        ),
    ]