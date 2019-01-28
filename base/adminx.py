from __future__ import absolute_import

import xadmin
from .models import Stock


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