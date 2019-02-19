from django.db import models

from django.utils.encoding import python_2_unicode_compatible

CN_MARKET = (
    ('SH', u"沪市"),
    ('SZ', u"深市"),
)


# Create your models here.
@python_2_unicode_compatible
class Stock(models.Model):
    co_name = models.CharField(max_length=16, verbose_name=u'名称')
    symbol = models.CharField(max_length=16, verbose_name=u'编号')
    market = models.CharField(max_length=16, choices=CN_MARKET, verbose_name=u'市场')
    asset = models.CharField(max_length=64, verbose_name=u'价值')
    co_business = models.CharField(max_length=64, verbose_name=u'板块')
    cc = models.CharField(max_length=64, verbose_name=u'市值')
    amplitude = models.CharField(max_length=64, verbose_name=u'流通')
    pe_s_d = models.CharField(max_length=64, verbose_name=u'pe_s_d')
    co_intro = models.TextField(verbose_name=u'基本信息')
    exchange = models.CharField(max_length=64, verbose_name=u'交易所', choices=CN_MARKET, )
    mv = models.CharField(max_length=64, verbose_name=u'总市值')
    pb_d = models.CharField(max_length=64, verbose_name=u'pb_d')
    ps_d = models.CharField(max_length=64, verbose_name=u'ps_d')
    equity = models.CharField(max_length=64, verbose_name=u'equity')
    industry = models.CharField(max_length=64, verbose_name=u'板块')

    class Meta:
        verbose_name = u"股票"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '股票: %s' % self.co_name


@python_2_unicode_compatible
class RunBase(models.Model):
    name = models.CharField(verbose_name=u"名称", max_length=64)
    start = models.DateField(verbose_name=u"开始")
    end = models.DateField(verbose_name=u"结束")
    description = models.TextField(verbose_name=u"说明", blank=True)
    status = models.CharField(verbose_name=u"状态", max_length=64, blank=True, default="新建")

    read_cash = models.IntegerField(verbose_name=u"初始化资金")

    stocks = models.ManyToManyField(
        Stock, verbose_name=u'股票组合', blank=True, related_name='stock_groups')
