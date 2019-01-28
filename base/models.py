from django.db import models

from django.utils.encoding import python_2_unicode_compatible


CN_MARKET = (
    ('SH', u"沪市"),
    ('SZ', u"深市"),
)

# Create your models here.
@python_2_unicode_compatible
class Stock(models.Model):
    co_name = models.CharField(max_length=64, verbose_name=u'名称')
    symbol = models.CharField(max_length=64, verbose_name=u'编号')
    market = models.CharField(max_length=64, choices=CN_MARKET, verbose_name=u'市场')
    # asset = models.CharField(max_length=64, verbose_name=u'价值')
    # co_business = models.CharField(max_length=64, verbose_name=u'板块')
    # cc = models.CharField(max_length=64, verbose_name=u'市值')
    # pe_s_d = models.CharField(max_length=64, verbose_name=u'市值')
    # co_intro = models.CharField(max_length=64, verbose_name=u'市值')
    # exchange = models.CharField(max_length=64, verbose_name=u'市值')
    # mv = models.CharField(max_length=64, verbose_name=u'市值')
    # pb_d = models.CharField(max_length=64, verbose_name=u'市值')
    # ps_d = models.CharField(max_length=64, verbose_name=u'市值')
    # equity = models.CharField(max_length=64, verbose_name=u'市值')
    # industry = models.CharField(max_length=64, verbose_name=u'市值')

    class Meta:
        verbose_name = u"股票"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '股票: %s' % self.co_name