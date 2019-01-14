from django.db import models

from django.utils.encoding import python_2_unicode_compatible


# Create your models here.
@python_2_unicode_compatible
class Stock(models.Model):
    name = models.CharField(max_length=64, verbose_name=u'名称')

    class Meta:
        verbose_name = u"股票"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '股票: %s' % self.name