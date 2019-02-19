from __future__ import absolute_import

from django.utils.translation import ugettext as _

import xadmin
from .models import FactorBuyBreakXd, FactorBuyDoubleMa, \
    FactorBuySDBreak, FactorBuyWD, WeekMonthBuy, DownUpTrend

ACTION_NAME = {
    'add': _('Can add %s'),
    'change': _('Can change %s'),
    'edit': _('Can edit %s'),
    'delete': _('Can delete %s'),
    'view': _('Can view %s'),
}


@xadmin.sites.register(FactorBuyBreakXd)
class FactorBuyBreakXdAdmin(object):
    list_display = ("name", "xd")

    list_display_links = ("name",)

    search_fields = ["name"]

    list_filter = [
        "name"
    ]

    list_quick_filter = [{"field": "name", "limit": 10}]

    search_fields = ["name"]

    reversion_enable = True


@xadmin.sites.register(FactorBuyDoubleMa)
class FactorBuyDoubleMaAdmin(object):
    list_display = ("name", "slow_int", "fast_int")

    list_display_links = ("name",)

    search_fields = ["name"]

    list_filter = [
        "name"
    ]

    list_quick_filter = [{"field": "name", "limit": 10}]

    search_fields = ["name"]

    reversion_enable = True


@xadmin.sites.register(FactorBuySDBreak)
class FactorBuySDBreakAdmin(object):
    list_display = ("name", "xd", "poly")

    list_display_links = ("name",)

    search_fields = ["name"]

    list_filter = [
        "name"
    ]

    list_quick_filter = [{"field": "name", "limit": 10}]

    search_fields = ["name"]

    reversion_enable = True


@xadmin.sites.register(FactorBuyWD)
class FactorBuyWDAdmin(object):
    list_display = ("name", "buy_dw", "buy_dwm", 'dw_period',)

    list_display_links = ("name",)

    search_fields = ["name"]

    list_filter = [
        "name"
    ]

    list_quick_filter = [{"field": "name", "limit": 10}]

    search_fields = ["name"]

    reversion_enable = True

@xadmin.sites.register(WeekMonthBuy)
class WeekMonthBuyAdmin(object):
    list_display = ("name", "is_buy_month_box",)

    list_display_links = ("name",)

    search_fields = ["name"]

    list_filter = [
        "name"
    ]

    list_quick_filter = [{"field": "name", "limit": 10}]

    search_fields = ["name"]

    reversion_enable = True

@xadmin.sites.register(DownUpTrend)
class DownUpTrendAdmin(object):
    list_display = ("name", "xd", "past_factor", "down_deg_threshold",)

    list_display_links = ("name",)

    search_fields = ["name"]

    list_filter = [
        "name"
    ]

    list_quick_filter = [{"field": "name", "limit": 10}]

    search_fields = ["name"]

    reversion_enable = True
