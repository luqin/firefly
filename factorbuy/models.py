from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from django.conf import settings
from django.utils.encoding import python_2_unicode_compatible

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


# Create your models here.
@python_2_unicode_compatible
class FactorBuy(models.Model):
    name = models.CharField(max_length=64, verbose_name=u'名称')
    factor_name = models.CharField(max_length=64, verbose_name=u'策略名称', editable=False)
    class_name = models.CharField(max_length=256, verbose_name=u'策略', editable=False)

    class Meta:
        verbose_name = u"买策略"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '策略: %s, 名称: %s' % (self.factor_name, self.name)


@python_2_unicode_compatible
class FactorBuyBreakXd(FactorBuy):
    """
    海龟向上趋势突破买入策略:趋势突破定义为当天收盘价格超过N天内的最高价，超过最高价格作为买入信号买入股票持有
    """
    xd = models.IntegerField(verbose_name=u"周期")

    class Meta:
        verbose_name = u"海龟买入"
        verbose_name_plural = verbose_name

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.class_name = "{'xd': %s, 'class': AbuFactorBuyBreak}" % self.xd
        self.factor_name = self._meta.verbose_name
        super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return '策略名称: %s, 周期: %s' % (self.name, self.xd)


@python_2_unicode_compatible
class FactorBuyDoubleMa(FactorBuy):
    """
    动态自适应双均线买入策略：
    双均线策略是量化策略中经典的策略之一，其属于趋势跟踪策略:
        1. 预设两条均线：如一个ma=5，一个ma=60, 5的均线被称作快线，60的均线被称作慢线
        2. 择时买入策略中当快线上穿慢线（ma5上穿ma60）称为形成金叉买点信号，买入股票
        3. 自适应动态慢线，不需要输入慢线值，根据走势震荡套利空间，寻找合适的ma慢线
        4. 自适应动态快线，不需要输入快线值，根据慢线以及大盘走势，寻找合适的ma快线
    """
    slow_int = models.IntegerField(verbose_name=u"慢线")
    fast_int = models.IntegerField(verbose_name=u"快线(-1:为自动)")

    class Meta:
        verbose_name = u"双均线买"
        verbose_name_plural = verbose_name

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.class_name = "{'slow': %d, 'fast': %d, 'class': AbuDoubleMaBuy}" % (self.slow_int, self.fast_int)
        self.factor_name = self._meta.verbose_name
        super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return '策略:%s, 名称: %s, 短周期: %s, 长周期: %s' % (self._meta.verbose_name, self.name, self.slow_int, self.fast_int)


@python_2_unicode_compatible
class FactorBuySDBreak(FactorBuyBreakXd):
    """
    参照大盘走势向上趋势突破买入策略：
        在海龟突破基础上，参照大盘走势，进行降低交易频率，提高系统的稳定性处理，当大盘走势震荡时封锁交易，
        当大盘走势平稳时再次打开交易，每一个月计算一次大盘走势是否平稳
    """
    poly = models.IntegerField(verbose_name=u"拟合")

    class Meta:
        verbose_name = u"平稳突破买"
        verbose_name_plural = verbose_name

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.class_name = "{'poly': %d, 'xd': %d, 'class': AbuSDBreak}" % (self.poly, self.xd)
        self.factor_name = self._meta.verbose_name
        super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return '策略:%s, 名称: %s, %s 拟合 %s 天趋势突破参照大盘' % (self._meta.verbose_name, self.name, self.poly, self.xd)


@python_2_unicode_compatible
class FactorBuyWD(FactorBuy):
    """
    日胜率均值回复策略：
        1. 默认以40天为周期(8周)结合涨跌阀值计算周几适合买入
        2. 回测运行中每一月重新计算一次上述的周几适合买入
        3. 在策略日任务中买入信号为：昨天下跌，今天开盘也下跌，且明天是计算出来的上涨概率大的'周几'
    """
    buy_dw = models.FloatField(verbose_name=u"胜率", default=0.55,
                               validators=[MinValueValidator(0.5), MaxValueValidator(0.99)], )
    buy_dwm = models.FloatField(verbose_name=u"系数", validators=[MinValueValidator(0.5), MaxValueValidator(1.0)],
                                default=0.618)
    dw_period = models.IntegerField(verbose_name=u"周期", validators=[MinValueValidator(20), MaxValueValidator(120), ],
                                    default=40)

    class Meta:
        verbose_name = u"周涨胜率"
        verbose_name_plural = verbose_name

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.class_name = "{'buy_dw': %f, 'buy_dwm': %f, 'dw_period': %d, 'class': AbuFactorBuyWD}" % (
            self.buy_dw, self.buy_dwm, self.dw_period)
        self.factor_name = self._meta.verbose_name
        super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return '策略:%s, 名称: %s, 日胜率%s,%s,%s均值回复买入' % (
            self._meta.verbose_name, self.name, self.buy_dw, self.buy_dwm, self.dw_period)


@python_2_unicode_compatible
class WeekMonthBuy(FactorBuy):
    BUY_MONTH = (
        (True, u"定期一个月"),
        (False, u"定期一个周"),
    )

    """
    固定周期买入策略：
      根据参数每周买入一次或者每一个月买入一次
      需要与特定\'选股策略\'和\'卖出策略\'形成配合\'
      单独使用固定周期买入策略意义不大
    """
    is_buy_month_box = models.BooleanField(verbose_name=u"定期时长", choices=BUY_MONTH, )

    class Meta:
        verbose_name = u"定期买入"
        verbose_name_plural = verbose_name

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.class_name = "{'is_buy_month_box': %s, 'class': AbuWeekMonthBuy}" % (self.is_buy_month_box,)
        self.factor_name = self._meta.verbose_name
        super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return '策略:%s, 名称: %s, %s买入一次' % (
            self._meta.verbose_name, self.name, u'每一月' if self.is_buy_month_box else u'每一周')


@python_2_unicode_compatible
class DownUpTrend(FactorBuy):
    """
    整个择时周期分成两部分，长的为长线择时，短的为短线择时：
      1. 寻找长线下跌的股票，比如一个季度(4个月)整体趋势为下跌趋势
      2. 短线走势上涨的股票，比如一个月整体趋势为上涨趋势，
      3. 最后使用海龟突破的N日突破策略作为策略最终买入信号
    """
    xd = models.SmallIntegerField(verbose_name=u"短线周期", choices=[(i, "%s 天" % i) for i in range(5, 120, 5)],
                                  validators=[MinValueValidator(5), MaxValueValidator(120), ], default=20)
    past_factor = models.SmallIntegerField(verbose_name=u"长线乘数(长线乘数：短线基础 x 长线乘数 = 长线周期)",
                                           choices=[(i, "%s " % i) for i in range(5, 120, 5)],
                                           validators=[MinValueValidator(1), MaxValueValidator(10), ], default=4)
    down_deg_threshold = models.SmallIntegerField(verbose_name=u"角度阀值(拟合趋势角度阀值：如-2,-3,-4)",
                                                  validators=[MinValueValidator(-10), MaxValueValidator(0), ],
                                                  choices=[(i, "%s " % i) for i in range(-10, 0, 1)], default=-3)

    class Meta:
        verbose_name = u"长跌短涨"
        verbose_name_plural = verbose_name

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.class_name = "{'xd': %d, 'past_factor': %d, 'down_deg_threshold': %d,'class': AbuDownUpTrend}" % (
            self.xd, self.past_factor, self.down_deg_threshold)
        self.factor_name = self._meta.verbose_name
        super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return '策略:%s, 名称: %s, 长线 %s 下跌短线 %s 上涨角度 %s' % (
            self._meta.verbose_name, self.name, self.xd, self.past_factor, self.down_deg_threshold)
