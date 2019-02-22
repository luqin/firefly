from __future__ import absolute_import

from django.forms import ModelMultipleChoiceField
from django.utils.translation import ugettext as _

import xadmin
from .xadmin_action import RunloopAction
from .models import RunLoopGroup, Orders

ACTION_NAME = {
    'add': _('Can add %s'),
    'change': _('Can change %s'),
    'edit': _('Can edit %s'),
    'delete': _('Can delete %s'),
    'view': _('Can view %s'),
}

def get_stock_name(p):
    action = p.codename.split('_')[0]
    if action in ACTION_NAME:
        return ACTION_NAME[action] % str(p.content_type)
    else:
        return p.co_name


class StockModelMultipleChoiceField(ModelMultipleChoiceField):

    def label_from_instance(self, p):
        return get_stock_name(p)

@xadmin.sites.register(RunLoopGroup)
class RunLoopGroupAdmin(object):
    list_display = ("name", "start", "end", "status", "description", 'link',)
    list_display_links = ("name",)
    # readony_fields = ("status", )
    exclude = ['status']

    list_quick_filter = [{"field": "name", "limit": 10}]

    search_fields = ["name"]

    reversion_enable = True

    style_fields = {"factor_buys": "checkbox-inline", "factor_sells": "checkbox-inline", "positions": "radio-inline",
                    "stocks": "m2m_transfer"}

    # def get_field_attrs(self, db_field, **kwargs):
    #     print("db_field", db_field)
    #     attrs = super(RunLoopGroupAdmin, self).get_field_attrs(db_field, **kwargs)
    #     if db_field.name == 'stocks':
    #         attrs['form_class'] = StockModelMultipleChoiceField
    #     return attrs

    actions = [RunloopAction]

    def link(self, instance):
        if instance.status == 'done':
            return "<a href='%s/k' target='_blank'>%s</a>" % (instance.id, '查看')
        else:
            return ""
    link.short_description = "回测结果"
    link.allow_tags = True
    link.is_column = False


@xadmin.sites.register(Orders)
class OrdersAdmin(object):
    list_display = (
        "run_loop_group", "stock", "profit", "profit_cg_hunder", "buy_date", "buy_price", "buy_cnt", "buy_factor",
        "sell_date", "sell_price", "sell_type_extra", "sell_type")
    list_display_links = ("stock",)
    # readony_fields = ("status", )
    # exclude = ['status']

    list_quick_filter = [{"field": "stock", "limit": 10}]

    search_fields = ["stock"]

    reversion_enable = True

# xadmin.sites.site.register(HostGroup, HostGroupAdmin)
# xadmin.sites.site.register(MaintainLog, MaintainLogAdmin)
# xadmin.sites.site.register(IDC, IDCAdmin)
# xadmin.sites.site.register(AccessRecord, AccessRecordAdmin)
