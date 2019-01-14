from django.db import models

from django.conf import settings
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _, ugettext

from base.models import Stock

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')

FACTOR_BUY_CLASSES = (
    ('AbuFactorBuyBreak', u"海龟买"),
    ('AbuDoubleMaBuy', u"双均线买"),
)

FACTOR_SELL_CLASSES = (
    ('AbuFactorSellBreak', u"海龟卖"),
    ('AbuDoubleMaSell', u"双均线卖"),
)


# class FactorBuyManager(models.Manager):
#     def create(self, **kwargs):
#
#         return super().create(**kwargs)


# Create your models here.
@python_2_unicode_compatible
class FactorBuy(models.Model):
    name = models.CharField(max_length=64, verbose_name=u'名称')
    class_name = models.CharField(max_length=32, choices=FACTOR_BUY_CLASSES, verbose_name=u'策略', editable=False)

    class Meta:
        verbose_name = u"买策略"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '策略名称: %s' % self.name


# Create your models here.
@python_2_unicode_compatible
class FactorSell(models.Model):
    name = models.CharField(max_length=64, verbose_name=u'名称')
    class_name = models.CharField(max_length=32, choices=FACTOR_SELL_CLASSES, verbose_name=u'策略', editable=False)

    class Meta:
        verbose_name = u"卖策略"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '策略名称: %s' % self.name


@python_2_unicode_compatible
class FactorBuyBreakXd(FactorBuy):
    """
    海龟向上趋势突破买入策略:趋势突破定义为当天收盘价格超过N天内的最高价，超过最高价格作为买入信号买入股票持有
    """
    xd = models.CharField(verbose_name=u"周期", max_length=64)

    class Meta:
        verbose_name = u"海龟买入"
        verbose_name_plural = verbose_name

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.class_name = "AbuFactorBuyBreak"
        super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return '策略名称: %s, 周期: %s' % (self.name, self.xd)


@python_2_unicode_compatible
class FactorSellBreakXd(FactorSell):
    """
    海龟向上趋势突破买入策略:趋势突破定义为当天收盘价格超过N天内的最高价，超过最高价格作为买入信号买入股票持有
    """
    xd = models.CharField(verbose_name=u"周期", max_length=64)

    class Meta:
        verbose_name = u"海龟卖出"
        verbose_name_plural = verbose_name

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.class_name = "AbuFactorSellBreak"
        super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return '策略名称: %s, 周期: %s' % (self.name, self.xd)


@python_2_unicode_compatible
class RunLoopGroup(models.Model):
    name = models.CharField(verbose_name=u"名称", max_length=64)
    description = models.TextField(verbose_name=u"说明")
    status = models.CharField(verbose_name=u"状态", max_length=64, blank=True, default="新建")

    factor_buys = models.ManyToManyField(
        FactorBuy, verbose_name=u'买策略组合', blank=False, related_name='factor_buy_groups')
    factor_sells = models.ManyToManyField(
        FactorSell, verbose_name=u'卖策略组合', blank=False, related_name='factor_sell_groups')
    stocks = models.ManyToManyField(
        Stock, verbose_name=u'股票组合', blank=False, related_name='stock_groups')

    class Meta:
        verbose_name = u"回测"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '回测名称: %s' % (self.name,)
