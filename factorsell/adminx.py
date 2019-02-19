from __future__ import absolute_import

from django.utils.translation import ugettext as _

import xadmin
from .models import FactorSellBreakXd, FactorSellDoubleMa, FactorSellAtrNStop, FactorSellCloseAtrN, \
    FactorSellPreAtrNStop, FactorSellNDay

ACTION_NAME = {
    'add': _('Can add %s'),
    'change': _('Can change %s'),
    'edit': _('Can edit %s'),
    'delete': _('Can delete %s'),
    'view': _('Can view %s'),
}


@xadmin.sites.register(FactorSellBreakXd)
class FactorSellBreakXdAdmin(object):
    list_display = ("name", "xd")

    list_display_links = ("name",)

    search_fields = ["name"]

    list_filter = [
        "name"
    ]

    list_quick_filter = [{"field": "name", "limit": 10}]

    search_fields = ["name"]

    reversion_enable = True


@xadmin.sites.register(FactorSellDoubleMa)
class FactorSellDoubleMaAdmin(object):
    list_display = ("name", "slow_int", "fast_int")

    list_display_links = ("name",)

    search_fields = ["name"]

    list_filter = [
        "name"
    ]

    list_quick_filter = [{"field": "name", "limit": 10}]

    search_fields = ["name"]

    reversion_enable = True


@xadmin.sites.register(FactorSellAtrNStop)
class FactorSellAtrNStopAdmin(object):
    list_display = ("name", "stop_loss_n", "stop_win_n",)

    list_display_links = ("name",)

    search_fields = ["name"]

    list_filter = [
        "name"
    ]

    list_quick_filter = [{"field": "name", "limit": 10}]

    search_fields = ["name"]

    reversion_enable = True


@xadmin.sites.register(FactorSellCloseAtrN)
class FactorSellCloseAtrNAdmin(object):
    list_display = ("name", "close_atr_n",)

    list_display_links = ("name",)

    search_fields = ["name"]

    list_filter = [
        "name"
    ]

    list_quick_filter = [{"field": "name", "limit": 10}]

    search_fields = ["name"]

    reversion_enable = True


@xadmin.sites.register(FactorSellPreAtrNStop)
class FactorSellPreAtrNStopAdmin(object):
    list_display = ("name", "pre_atr_n",)

    list_display_links = ("name",)

    search_fields = ["name"]

    list_filter = [
        "name"
    ]

    list_quick_filter = [{"field": "name", "limit": 10}]

    search_fields = ["name"]

    reversion_enable = True

@xadmin.sites.register(FactorSellNDay)
class FactorSellNDayAdmin(object):
    list_display = ("name", "sell_n","sell_n", "is_sell_today")

    list_display_links = ("name",)

    search_fields = ["name"]

    list_filter = [
        "name"
    ]

    list_quick_filter = [{"field": "name", "limit": 10}]

    search_fields = ["name"]

    reversion_enable = True
