from __future__ import absolute_import

import xadmin
from .models import Stock


@xadmin.sites.register(Stock)
class StockAdmin(object):
    list_display = ("name", )

    list_display_links = ("name",)

    search_fields = ["name"]

    list_filter = [
        "name"
    ]

    list_quick_filter = [{"field": "name", "limit": 10}]

    search_fields = ["name"]

    reversion_enable = True