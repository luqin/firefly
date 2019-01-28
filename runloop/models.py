from django.db import models

from django.conf import settings
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _, ugettext

from base.models import Stock

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')

FACTOR_BUY_CLASSES = (
    ('FactorBuyBreakXd', u"海龟买"),
    ('AbuDoubleMaBuy', u"双均线买"),
)

FACTOR_SELL_CLASSES = (
    ('FactorSellBreakXd', u"海龟卖"),
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
    class_name = models.CharField(max_length=256, choices=FACTOR_BUY_CLASSES, verbose_name=u'策略', editable=False)

    # def to_factor(self):
    #     return eval(self.class_name)

    class Meta:
        verbose_name = u"买策略"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '策略名称: %s' % self.name


# Create your models here.
@python_2_unicode_compatible
class FactorSell(models.Model):
    name = models.CharField(max_length=64, verbose_name=u'名称')
    class_name = models.CharField(max_length=256, choices=FACTOR_SELL_CLASSES, verbose_name=u'策略', editable=False)

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
        self.class_name = "{'xd': %s, 'class': AbuFactorBuyBreak}" % self.xd
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
        self.class_name = "{'xd': %s, 'class': AbuFactorSellBreak}" % self.xd
        super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return '策略名称: %s, 周期: %s' % (self.name, self.xd)


@python_2_unicode_compatible
class RunLoopGroup(models.Model):
    name = models.CharField(verbose_name=u"名称", max_length=64)
    start = models.DateField(verbose_name=u"开始")
    end = models.DateField(verbose_name=u"结束")
    description = models.TextField(verbose_name=u"说明",blank=True)
    status = models.CharField(verbose_name=u"状态", max_length=64, blank=True, default="新建")

    read_cash = models.IntegerField(verbose_name=u"初始化资金")

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
    run_loop_group = models.ForeignKey(RunLoopGroup, null=True, blank=True, on_delete=models.SET_NULL, verbose_name=u"回测")

    class Meta:
        verbose_name = u"回测订单"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '回测订单: %s' % (self.run_loop_group,)