from __future__ import absolute_import

from django.utils.translation import ugettext as _

import xadmin
from .xadmin_action import MyAction
from .models import RunLoopGroup, FactorBuy, FactorBuyBreakXd, FactorSellBreakXd

ACTION_NAME = {
    'add': _('Can add %s'),
    'change': _('Can change %s'),
    'edit': _('Can edit %s'),
    'delete': _('Can delete %s'),
    'view': _('Can view %s'),
}

# @xadmin.sites.register(FactorBuy)
# class FactorBuyAdmin(object):
#     list_display = ("name",)
#     list_display_links = ("name",)
#
#     list_quick_filter = [{"field": "name", "limit": 10}]
#
#     search_fields = ["name"]
#
#     reversion_enable = True


@xadmin.sites.register(FactorBuyBreakXd)
class FactorBuyBreakXdAdmin(object):
    list_display = ("name", "xd", "class_name")

    list_display_links = ("name",)

    search_fields = ["name"]

    list_filter = [
        "name"
    ]

    list_quick_filter = [{"field": "name", "limit": 10}]

    search_fields = ["name"]

    reversion_enable = True

@xadmin.sites.register(FactorSellBreakXd)
class FactorSellBreakXdAdmin(object):
    list_display = ("name", "xd", "class_name")

    list_display_links = ("name",)

    search_fields = ["name"]

    list_filter = [
        "name"
    ]

    list_quick_filter = [{"field": "name", "limit": 10}]

    search_fields = ["name"]

    reversion_enable = True

@xadmin.sites.register(RunLoopGroup)
class RunLoopGroupAdmin(object):
    list_display = ("name", "status", "description")
    list_display_links = ("name",)
    # readony_fields = ("status", )
    exclude = ['status']

    list_quick_filter = [{"field": "name", "limit": 10}]

    search_fields = ["name"]

    reversion_enable = True

    style_fields = {"factor_buys": "checkbox-inline","factor_sells": "checkbox-inline"}

    actions = [MyAction, ]

# xadmin.sites.site.register(HostGroup, HostGroupAdmin)
# xadmin.sites.site.register(MaintainLog, MaintainLogAdmin)
# xadmin.sites.site.register(IDC, IDCAdmin)
# xadmin.sites.site.register(AccessRecord, AccessRecordAdmin)
