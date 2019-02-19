from __future__ import absolute_import

from django.utils.translation import ugettext as _

import xadmin
from .xadmin_action import GridSearchAction
from .models import FactorBuyRangeBreakXd, \
    FactorSellRangeBreakXd, RunGridSearch

ACTION_NAME = {
    'add': _('Can add %s'),
    'change': _('Can change %s'),
    'edit': _('Can edit %s'),
    'delete': _('Can delete %s'),
    'view': _('Can view %s'),
}


@xadmin.sites.register(FactorBuyRangeBreakXd)
class FactorBuyRangeBreakXdAdmin(object):
    list_display = ("name", "start", "end", "step")

    list_display_links = ("name",)

    search_fields = ["name"]

    list_filter = [
        "name"
    ]

    list_quick_filter = [{"field": "name", "limit": 10}]

    search_fields = ["name"]

    reversion_enable = True


@xadmin.sites.register(FactorSellRangeBreakXd)
class FactorSellRangeBreakXdAdmin(object):
    list_display = ("name", "start", "end", "step")

    list_display_links = ("name",)

    search_fields = ["name"]

    list_filter = [
        "name"
    ]

    list_quick_filter = [{"field": "name", "limit": 10}]

    search_fields = ["name"]

    reversion_enable = True


@xadmin.sites.register(RunGridSearch)
class RunGridSearchAdmin(object):
    list_display = ("name", "start", "end", "status", "description")
    list_display_links = ("name",)
    # readony_fields = ("status", )
    exclude = ['status']

    list_quick_filter = [{"field": "name", "limit": 10}]

    search_fields = ["name"]

    reversion_enable = True

    style_fields = {"factor_buys": "checkbox-inline", "factor_sells": "checkbox-inline"}

    actions = [GridSearchAction]
