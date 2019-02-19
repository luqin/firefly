from abc import abstractmethod

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from django.conf import settings
from django.utils.encoding import python_2_unicode_compatible

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


# Create your models here.
@python_2_unicode_compatible
class FactorSell(models.Model):
    name = models.CharField(max_length=64, verbose_name=u'名称')
    factor_name = models.CharField(max_length=64, verbose_name=u'策略名称', editable=False)
    class_name = models.CharField(max_length=256, verbose_name=u'策略', editable=False)

    class Meta:
        verbose_name = u"卖策略"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '策略: %s, 名称: %s' % (self.factor_name, self.name)

    def delegate_class(self):
        """子类因子所委托的具体因子类"""
        pass


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
        self.factor_name = self._meta.verbose_name
        super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return '策略名称: %s, 周期: %s' % (self.name, self.xd)


@python_2_unicode_compatible
class FactorSellDoubleMa(FactorSell):
    """
    双均线卖出策略：
        双均线策略是量化策略中经典的策略之一，其属于趋势跟踪策略:
        1. 预设两条均线：如一个ma=5，一个ma=60, 5的均线被称作快线，60的均线被称作慢线
        2. 择时卖出策略中当快线下穿慢线（ma5下穿ma60）称为形成死叉卖点信号，卖出股票
    """
    slow_int = models.IntegerField(verbose_name=u"慢线")
    fast_int = models.IntegerField(verbose_name=u"快线")

    class Meta:
        verbose_name = u"双均线卖"
        verbose_name_plural = verbose_name

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.class_name = "{'slow': %d, 'fast': %d, 'class': AbuDoubleMaSell}" % (self.slow_int, self.fast_int)
        self.factor_name = self._meta.verbose_name
        super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return '策略:%s, 名称: %s, 短周期: %s, 长周期: %s' % (self._meta.verbose_name, self.name, self.slow_int, self.fast_int)


@python_2_unicode_compatible
class FactorSellAtrNStop(FactorSell):
    """
    止盈策略 & 止损策略：
      1. 真实波幅atr作为最大止盈和最大止损的常数值
      2. 当stop_loss_n 乘以 当日atr > 买入价格 － 当日收盘价格->止损卖出
      3. 当stop_win_n 乘以 当日atr < 当日收盘价格 －买入价格->止盈卖出
    """
    stop_loss_n = models.FloatField(verbose_name=u"止损(stop_loss_n乘以当日atr大于买价减close->止损)",
                                    validators=[MinValueValidator(0.1), MaxValueValidator(10.0)],
                                    default=1.0, )
    stop_win_n = models.FloatField(verbose_name=u"止盈(stop_win_n乘以当日atr小于close减买价->止盈)",
                                   validators=[MinValueValidator(0.1), MaxValueValidator(10.0)],
                                   default=3.0, )

    class Meta:
        verbose_name = u"止盈止损"
        verbose_name_plural = verbose_name

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.class_name = "{'stop_loss_n': %f, 'stop_win_n': %f, 'class': %s}" % (
            self.stop_loss_n, self.stop_win_n, self.delegate_class())
        self.factor_name = self._meta.verbose_name
        super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return '策略:%s, 名称: %s, n atr止盈 %f 止损 %f ' % (
            self._meta.verbose_name, self.name, self.stop_loss_n, self.stop_win_n)

    def delegate_class(self):
        return 'AbuFactorAtrNStop'


@python_2_unicode_compatible
class FactorSellCloseAtrN(FactorSell):
    """
    利润保护止盈策略：
      1. 买入后最大收益价格 - 今日价格 > 一定收益
      2. 买入后最大收益价格 - 今日价格 < close_atr_n * 当日atr
      3. 当买入有一定收益后，如果下跌幅度超过close_atr_n乘以当日atr->保护止盈卖出
    """
    close_atr_n = models.FloatField(verbose_name=u"止盈(收益下跌超过close_atr_n乘以当日atr->保护止盈)",
                                    validators=[MinValueValidator(0.1), MaxValueValidator(10.0)],
                                    default=1.5, )

    class Meta:
        verbose_name = u"保护止盈"
        verbose_name_plural = verbose_name

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.class_name = "{'close_atr_n': %f, 'class': %s}" % (self.close_atr_n, self.delegate_class())
        self.factor_name = self._meta.verbose_name
        super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return '策略:%s, 名称: %s, 利润保护止盈n= %f ' % (self._meta.verbose_name, self.name, self.close_atr_n)

    def delegate_class(self):
        return 'AbuFactorCloseAtrNStop'


@python_2_unicode_compatible
class FactorSellPreAtrNStop(FactorSell):
    """
    风险控制止损策略：
      1. 单日最大跌幅n倍atr止损
      2. 当今日价格下跌幅度 > 当日atr 乘以 pre_atr_n（下跌止损倍数）卖出操作
    """
    pre_atr_n = models.FloatField(verbose_name=u"止损(当今天价格开始剧烈下跌，采取果断平仓措施)",
                                  validators=[MinValueValidator(0.1), MaxValueValidator(10.0)],
                                  default=1.5, )

    class Meta:
        verbose_name = u"风险止损"
        verbose_name_plural = verbose_name

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.class_name = "{'pre_atr_n': %f, 'class': %s}" % (self.pre_atr_n, self.delegate_class())
        self.factor_name = self._meta.verbose_name
        super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return '策略:%s, 名称: %s, 风险控制止损n= %f ' % (self._meta.verbose_name, self.name, self.pre_atr_n)

    def delegate_class(self):
        return 'AbuFactorPreAtrNStop'


@python_2_unicode_compatible
class FactorSellNDay(FactorSell):
    """
    持有N天后卖出策略：
      卖出策略，不管交易现在什么结果，买入后只持有N天
      需要与特定\'买入策略\'形成配合
      单独使用N天卖出策略意义不大
    """
    SELL_TODAY = (
        (True, u"N天后当天卖出"),
        (False, u"N天后隔天卖出"),
    )

    sell_n = models.IntegerField(verbose_name=u"N天",
                                 default=1, )

    is_sell_today = models.BooleanField(verbose_name=u"当天隔天", choices=SELL_TODAY, )

    class Meta:
        verbose_name = u"N天卖出"
        verbose_name_plural = verbose_name

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.class_name = "{'sell_n': %f,'is_sell_today':%s, 'class': %s}" % (self.sell_n, self.is_sell_today, self.delegate_class())
        self.factor_name = self._meta.verbose_name
        super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return '策略:%s, 名称: %s, 持有%s天%s卖出 ' % (self._meta.verbose_name, self.name, self.sell_n, u'当天' if self.is_sell_today else u'隔天')

    def delegate_class(self):
        return 'AbuFactorSellNDay'
