from __future__ import absolute_import

import xadmin
from xadmin import views
from .models import Stock


class GlobalSettings(object):
    site_title = 'Firefly'  # 修改页眉
    site_footer = 'Firefly'  # 修改页脚


xadmin.site.register(views.CommAdminView, GlobalSettings)


@xadmin.sites.register(Stock)
class StockAdmin(object):
    list_display = ("co_name", "symbol", "market")

    list_display_links = ("co_name",)

    search_fields = ["co_name"]

    list_filter = [
        "co_name"
    ]

    list_quick_filter = [{"field": "co_name", "limit": 10}]

    search_fields = ["co_name"]

    reversion_enable = True