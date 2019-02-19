import numpy as np
from django.db import models

from django.conf import settings
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _, ugettext

from base.models import Stock, RunBase

from factorbuy.models import FactorBuy
from factorsell.models import FactorSell

from position.models import Position

from pickstock.models import PickStock

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


@python_2_unicode_compatible
class RunLoopGroup(RunBase):
    factor_buys = models.ManyToManyField(
        FactorBuy, verbose_name=u'买策略组合', blank=False, related_name='factor_buy_groups')
    factor_sells = models.ManyToManyField(
        FactorSell, verbose_name=u'卖策略组合', blank=False, related_name='factor_sell_groups')

    positions = models.ForeignKey(
        Position, verbose_name=u'仓位管理', null=True, blank=True, on_delete=models.SET_NULL)

    pick_stocks = models.ManyToManyField(
        PickStock, verbose_name=u'选股因子', blank=True, related_name='pick_stock_groups')

    class Meta:
        verbose_name = u"回测"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '回测名称: %s' % (self.name,)


@python_2_unicode_compatible
class Orders(models.Model):
    buy_date = models.CharField(verbose_name=u"买入日期", max_length=64)
    buy_price = models.CharField(verbose_name=u"买入价格", max_length=64)
    buy_cnt = models.CharField(verbose_name=u"买入数量", max_length=64)
    buy_factor = models.CharField(verbose_name=u"买入策略", max_length=64)
    symbol = models.CharField(verbose_name=u"股票编号", max_length=64)
    buy_pos = models.CharField(verbose_name=u"买入滑dian", max_length=64)
    buy_type_str = models.CharField(verbose_name=u"买入类型", max_length=64)
    expect_direction = models.CharField(verbose_name=u"预期方向", max_length=64)
    sell_type_extra = models.CharField(verbose_name=u"卖出策略", max_length=64)
    sell_date = models.CharField(verbose_name=u"卖出日期", max_length=64)
    sell_price = models.CharField(verbose_name=u"卖出价格", max_length=64)
    sell_type = models.CharField(verbose_name=u"卖出类型", max_length=64)
    ml_features = models.CharField(verbose_name=u"MLI特征", max_length=64, blank=True, null=True)
    key = models.CharField(verbose_name=u"关键字", max_length=64)
    profit = models.CharField(verbose_name=u"盈利", max_length=64)
    result = models.CharField(verbose_name=u"结果", max_length=64)
    profit_cg = models.CharField(verbose_name=u"盈利比", max_length=64)
    profit_cg_hunder = models.CharField(verbose_name=u"盈利率", max_length=64)
    keep_days = models.CharField(verbose_name=u"持股天数", max_length=64)

    stock = models.ForeignKey(Stock, null=True, blank=True, on_delete=models.SET_NULL, verbose_name=u"股票")
    run_loop_group = models.ForeignKey(RunLoopGroup, null=True, blank=True, on_delete=models.SET_NULL,
                                       verbose_name=u"回测")

    class Meta:
        verbose_name = u"回测订单"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '回测订单: %s' % (self.run_loop_group,)
