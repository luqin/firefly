from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from django.conf import settings
from django.utils.encoding import python_2_unicode_compatible

import numpy as np

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


# Create your models here.
@python_2_unicode_compatible
class PickStock(models.Model):
    name = models.CharField(max_length=64, verbose_name=u'名称')
    pick_stock_name = models.CharField(max_length=64, verbose_name=u'择股因子名称', editable=False)
    class_name = models.CharField(max_length=256, verbose_name=u'择股因子策略', editable=False)

    xd = models.SmallIntegerField(verbose_name=u"周期",
                                  choices=[(i, "%s " % i) for i in range(1, 252, 1)],
                                  validators=[MinValueValidator(1), MaxValueValidator(252), ], default=252)

    REVERSED_SELECT = (
        (True, u"反转选股结果"),
        (False, u"不反转"),
    )

    reversed = models.BooleanField(verbose_name=u"反转结果", choices=REVERSED_SELECT, )

    class Meta:
        verbose_name = u"择股因子"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '择股因子: %s, 名称: %s' % (self.pick_stock_name, self.name)

    def delegate_class(self):
        """子类因子所委托的具体因子类"""
        pass


@python_2_unicode_compatible
class PickRegressAngMinMaxPickStock(PickStock):
    PRICE_MIN_CK_SELECT = (
        (True, u"否"),
        (False, u"是"),
    )

    """
    拟合角度选股因子策略：
      将交易目标前期走势进行线性拟合计算一个角度，选中规则：
      1. 交易目标前期走势拟合角度 > 最小拟合角度
      2. 交易目标前期走势拟合角度 < 最大拟合角度
    """

    ang_min_float = models.IntegerField(verbose_name=u"最小(设定选股角度最小阀值，默认-5):", default=-5, )
    ang_min_ck = models.BooleanField(verbose_name=u"使用最小阀值", choices=PRICE_MIN_CK_SELECT, )

    ang_max_float = models.IntegerField(verbose_name=u"最大(设定选股角度最大阀值，默认5):", default=5, )
    ang_max_ck = models.BooleanField(verbose_name=u"使用最大阀值", choices=PRICE_MIN_CK_SELECT, )

    class Meta:
        verbose_name = u"角度选股"
        verbose_name_plural = verbose_name

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        ang_min_str = self.ang_min_float if self.ang_min_ck else -np.inf
        ang_max_str = self.ang_max_float if self.ang_max_ck else np.inf

        self.class_name = "{'xd': %d,'reversed': %s,'threshold_ang_min': %f,'threshold_ang_max': %s, 'class': %s}" % (
            self.xd, self.reversed, ang_min_str, ang_max_str, self.delegate_class())
        self.pick_stock_name = self._meta.verbose_name
        super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return '策略名称: %s, 角度选股最大:%s最小:%s,周期:%s,反转:%s ' % (
            self.name, self.ang_max_float, self.ang_min_float, self.xd, self.reversed)

    def delegate_class(self):
        return 'AbuPickRegressAngMinMax'


@python_2_unicode_compatible
class PriceMinMaxPickStock(PickStock):
    PRICE_MIN_CK_SELECT = (
        (True, u"否"),
        (False, u"是"),
    )

    """
    价格选股因子策略：
      根据交易目标的一段时间内收盘价格的最大，最小值进行选股，选中规则：
      1. 交易目标最小价格 > 最小价格阀值
      2. 交易目标最大价格 < 最大价格阀值
    """
    price_min = models.FloatField(verbose_name=u"最小:", default=15)
    price_min_ck = models.BooleanField(verbose_name=u"使用最小阀值", choices=PRICE_MIN_CK_SELECT, )
    price_max = models.FloatField(verbose_name=u"最大:", default=50)
    price_max_ck = models.BooleanField(verbose_name=u"使用最大阀值", choices=PRICE_MIN_CK_SELECT, )

    class Meta:
        verbose_name = u"价格选股"
        verbose_name_plural = verbose_name

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        price_min_str = self.price_min if self.price_min_ck else -np.inf
        price_max_str = self.price_max if self.price_max_ck else np.inf

        self.class_name = "{'xd': %d,'reversed': %s,'threshold_price_min': %f,'threshold_price_max': %s, 'class': %s}" % (
            self.xd, self.reversed, price_min_str, price_max_str, self.delegate_class())
        self.pick_stock_name = self._meta.verbose_name
        super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return '策略名称: %s, 价格选股最大:%s 最小:%s ,周期:%s ,反转:%s ' % (
            self.name, self.price_max, self.price_min, self.xd, self.reversed)

    def delegate_class(self):
        return 'AbuPickStockPriceMinMax'


@python_2_unicode_compatible
class ShiftDistancePickStock(PickStock):
    """
    位移路程比选股因子策略：
      将交易目标走势每月计算价格位移路程比，根据比值进行选股，选取波动程度不能太大，也不太小的目标：
      1. 定义位移路程比大于参数阀值的月份为大波动月
      2. 一年中大波动月数量 < 最大波动月个数
      3. 一年中大波动月数量 > 最小波动月个数
    """
    threshold_sd = models.FloatField(verbose_name=u"阀值:", default=2.0,
                                     validators=[MinValueValidator(1), MaxValueValidator(6), ], )
    min = models.IntegerField(verbose_name=u"范围-小:", default=1,
                              validators=[MinValueValidator(1), MaxValueValidator(10), ], )
    max = models.IntegerField(verbose_name=u"范围-大:", default=4,
                              validators=[MinValueValidator(1), MaxValueValidator(10), ], )

    class Meta:
        verbose_name = u"位移路程"
        verbose_name_plural = verbose_name

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.class_name = "{'threshold_sd': %f,'reversed': %s,'threshold_max_cnt': %d,'threshold_min_cnt': %d, 'class': %s}" % (
            self.threshold_sd, self.reversed, self.max, self.min, self.delegate_class())
        self.pick_stock_name = self._meta.verbose_name
        super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return '策略名称: %s, 位移路程选股大波动:%s 最大:%s 最小:%s ,反转:%s ' % (
            self.name, self.threshold_sd, self.max, self.min, self.reversed)

    def delegate_class(self):
        return 'AbuPickStockShiftDistance'


@python_2_unicode_compatible
class PickStockNTopPickStock(PickStock):
    """
    涨跌幅top N选股因子策略：
      选股周期上对多只股票涨跌幅进行排序，选取top n个股票做为交易目标：
      (只对在股池中选定的symbol序列生效，对全市场回测暂时不生效)

      默认值为正：即选取涨幅最高的n_top个股票
      可设置为负：即选取跌幅最高的n_top个股票
    """

    DIRECTION_TOP_SELECT = (
        (1, u"正(涨幅)"),
        (-1, u"负(跌幅)"),
    )

    n_top = models.IntegerField(verbose_name=u"TOP N:", default=3,
                                validators=[MinValueValidator(1), MaxValueValidator(10), ], )
    direction_top = models.IntegerField(verbose_name=u"选取方向", choices=DIRECTION_TOP_SELECT, default=1)

    class Meta:
        verbose_name = u"top N涨跌"
        verbose_name_plural = verbose_name

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.class_name = "{'xd': %f,'reversed': %s,'n_top': %d,'direction_top': %d, 'class': %s}" % (
            self.xd, self.reversed, self.n_top, self.direction_top, self.delegate_class())
        self.pick_stock_name = self._meta.verbose_name
        super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return '策略名称: %s, 涨跌幅选股n_top:%s,方向:%s,xd:%s,反转:%s ' % (
            self.name, self.n_top, self.direction_top, self.xd, self.reversed)

    def delegate_class(self):
        return 'AbuPickStockNTop'
