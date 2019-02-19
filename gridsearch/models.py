import numpy as np
from django.db import models

from django.conf import settings
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _, ugettext

from base.models import Stock, RunBase

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')

FACTOR_BUY_CLASSES = (
    ('FactorBuyBreakXd', u"海龟买"),
    ('AbuDoubleMaBuy', u"双均线买"),
)

FACTOR_SELL_CLASSES = (
    ('FactorSellBreakXd', u"海龟卖"),
    ('AbuDoubleMaSell', u"双均线卖"),
)


@python_2_unicode_compatible
class Range(models.Model):
    name = models.CharField(max_length=64, verbose_name=u'名称')
    start = models.IntegerField(verbose_name=u"开始")
    end = models.IntegerField(verbose_name=u"结束")
    step = models.FloatField(verbose_name=u"增量")
    class_name = models.CharField(max_length=256, choices=FACTOR_SELL_CLASSES, verbose_name=u'策略', editable=False)

    class Meta:
        abstract = True

    def __str__(self):
        return '策略名称: %s' % self.name

@python_2_unicode_compatible
class RangeBuy(Range):
    pass

@python_2_unicode_compatible
class RangeSell(Range):
    pass

@python_2_unicode_compatible
class FactorBuyRangeBreakXd(RangeBuy):

    class Meta:
        verbose_name = u"海龟买入范围"
        verbose_name_plural = verbose_name

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.class_name = "{'xd': np.arange(%d, %d, %d), 'class': [AbuFactorBuyBreak]}" % (self.start, self.end, self.step)
        super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return '策略名称: %s, 周期: np.arange(%d, %d, %d)' % (self.name, self.start, self.end, self.step)


@python_2_unicode_compatible
class FactorSellRangeBreakXd(RangeSell):

    class Meta:
        verbose_name = u"海龟卖出范围"
        verbose_name_plural = verbose_name

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.class_name = "{'xd': np.arange(%d, %d, %d), 'class': [AbuFactorSellBreak]}" % (self.start, self.end, self.step)
        super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return '策略名称: %s, 周期: np.arange(%d, %d, %d)' % (self.name, self.start, self.end, self.step)


@python_2_unicode_compatible
class RunGridSearch(RunBase):

    factor_buys = models.ManyToManyField(
        RangeBuy, verbose_name=u'买策略组合', blank=False, related_name='factor_buy_groups')
    factor_sells = models.ManyToManyField(
        RangeSell, verbose_name=u'卖策略组合', blank=False, related_name='factor_sell_groups')


    class Meta:
        verbose_name = u"GridSearch"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '参数调优: %s' % (self.name,)