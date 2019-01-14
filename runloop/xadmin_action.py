from django.http import HttpResponse
from xadmin.plugins.actions import BaseActionView


class MyAction(BaseActionView):
    # 这里需要填写三个属性
    action_name = "change_sss"  #: 相当于这个 Action 的唯一标示, 尽量用比较针对性的名字
    description = u'Test selected %(verbose_name_plural)s'  #: 描述, 出现在 Action 菜单中, 可以使用 ``%(verbose_name_plural)s`` 代替 Model 的名字.
    model_perm = 'change'

    def do_action(self, queryset):
        for obj in queryset:
            # 其实我们做的只有这一部分 ********
            obj.status = 'run...'
            obj.save()
        # return HttpResponse('{"status": "success", "msg": "error"}', content_type='application/json')
