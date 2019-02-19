from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from django.conf import settings
from django.utils.encoding import python_2_unicode_compatible

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


# Create your models here.
@python_2_unicode_compatible
class Position(models.Model):
    name = models.CharField(max_length=64, verbose_name=u'名称')
    position_name = models.CharField(max_length=64, verbose_name=u'仓位策略名称', editable=False)
    class_name = models.CharField(max_length=256, verbose_name=u'仓位策略', editable=False)

    class Meta:
        verbose_name = u"仓位策略"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '仓位策略: %s, 名称: %s' % (self.position_name, self.name)

    def delegate_class(self):
        """子类因子所委托的具体因子类"""
        pass


@python_2_unicode_compatible
class KellyPosition(Position):
    """
    kelly仓位管理类 通过kelly公司计算仓位, fit_position计算的结果是买入多少个单位（股，手，顿，合约）
    """
    win_rate = models.FloatField(verbose_name=u"默认kelly仓位胜率0.50")
    gains_mean = models.FloatField(verbose_name=u"默认平均获利期望0.10")
    losses_mean = models.FloatField(verbose_name=u"默认平均亏损期望0.05")

    class Meta:
        verbose_name = u"kelly仓位管理"
        verbose_name_plural = verbose_name

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.class_name = "{'win_rate': %s,'gains_mean': %s,'losses_mean': %s, 'class': %s}" % (
            self.win_rate, self.gains_mean, self.losses_mean, self.delegate_class())
        self.position_name = self._meta.verbose_name
        super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return '策略名称: %s, 胜率: %s, 平均获利期望: %s, 平均亏损期望: %s' % (
            self.name, self.win_rate, self.gains_mean, self.losses_mean)

    def delegate_class(self):
        return 'AbuKellyPosition'


@python_2_unicode_compatible
class AtrPosPosition(Position):
    """
    atr资金仓位管理策略：
      默认的仓位资金管理全局策略
      根据决策买入当天的价格波动决策资金仓位配比
      注意不同于卖策，选股，一个买入因子只能有唯一个资金仓位管理策略
    """
    atr_pos_base = models.FloatField(verbose_name=u"基配",
                                     validators=[MinValueValidator(0.00001), MaxValueValidator(1.0)],
                                     default=0.1, )
    atr_base_price = models.SmallIntegerField(verbose_name=u"常价",
                                              choices=[(i, "%s " % i) for i in range(12, 20, 1)],
                                              validators=[MinValueValidator(12), MaxValueValidator(20), ], default=15)

    class Meta:
        verbose_name = u"atr资管"
        verbose_name_plural = verbose_name

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.class_name = "{'atr_pos_base': %f,'atr_base_price': %f, 'class': %s}" % (
            self.atr_pos_base, self.atr_base_price, self.delegate_class())
        self.position_name = self._meta.verbose_name
        super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return '策略名称: %s, atr资管仓位基数:%s 常数价格:%s' % (
            self.name, self.atr_pos_base, self.atr_base_price)

    def delegate_class(self):
        return 'AbuAtrPosition'


@python_2_unicode_compatible
class PtPosition(Position):
    """
    价格位置仓位管理策略：
      针对均值回复类型策略的仓位管理策略
      根据买入价格在之前一段时间的价格位置来决策仓位大小
      假设过去一段时间的价格为[10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
      如果当前买入价格为2元：则买入仓位配比很高(认为均值回复有很大向上空间)
      如果当前买入价格为9元：则买入仓位配比很低(认为均值回复向上空间比较小)
    """
    pos_base = models.FloatField(verbose_name=u"基配",
                                 validators=[MinValueValidator(0.00001), MaxValueValidator(1.0)],
                                 default=0.1, )
    past_day_cnt = models.SmallIntegerField(verbose_name=u"参考天数",
                                            choices=[(i, "%s " % i) for i in range(5, 250, 1)],
                                            validators=[MinValueValidator(5), MaxValueValidator(250), ], default=20)

    class Meta:
        verbose_name = u"价格位置"
        verbose_name_plural = verbose_name

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.class_name = "{'pos_base': %f,'past_day_cnt': %f, 'class': %s}" % (
            self.pos_base, self.past_day_cnt, self.delegate_class())
        self.position_name = self._meta.verbose_name
        super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return '策略名称: %s, 价格位置基仓比例:%s 参考天数:%s' % (
            self.name, self.pos_base, self.past_day_cnt)

    def delegate_class(self):
        return 'AbuPtPosition'
