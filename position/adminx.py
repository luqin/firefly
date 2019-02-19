from __future__ import absolute_import

from django.utils.translation import ugettext as _

import xadmin
from .models import KellyPosition, AtrPosPosition, PtPosition

ACTION_NAME = {
    'add': _('Can add %s'),
    'change': _('Can change %s'),
    'edit': _('Can edit %s'),
    'delete': _('Can delete %s'),
    'view': _('Can view %s'),
}


@xadmin.sites.register(KellyPosition)
class KellyPositionAdmin(object):
    list_display = ("name", "win_rate", "gains_mean", "losses_mean")

    list_display_links = ("name",)

    search_fields = ["name"]

    list_filter = [
        "name"
    ]

    list_quick_filter = [{"field": "name", "limit": 10}]

    search_fields = ["name"]

    reversion_enable = True


@xadmin.sites.register(AtrPosPosition)
class AtrPosPositionAdmin(object):
    list_display = ("name", "atr_pos_base", "atr_base_price", )

    list_display_links = ("name",)

    search_fields = ["name"]

    list_filter = [
        "name"
    ]

    list_quick_filter = [{"field": "name", "limit": 10}]

    search_fields = ["name"]

    reversion_enable = True


@xadmin.sites.register(PtPosition)
class PtPositionAdmin(object):
    list_display = ("name", "pos_base", "past_day_cnt", )

    list_display_links = ("name",)

    search_fields = ["name"]

    list_filter = [
        "name"
    ]

    list_quick_filter = [{"field": "name", "limit": 10}]

    search_fields = ["name"]

    reversion_enable = True