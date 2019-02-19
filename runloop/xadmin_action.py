import os
import threading

import abupy
import numpy as np
from abupy import AbuFactorBuyBreak, AbuBenchmark, AbuCapital, ABuPickTimeExecute, AbuMetricsBase, AbuFactorAtrNStop, \
    AbuFactorCloseAtrNStop, \
    AbuFactorPreAtrNStop, AbuFactorSellBreak, ABuGridHelper, GridSearch, ABuFileUtil, WrsmScorer, EMarketSourceType, \
    AbuDoubleMaBuy, AbuDoubleMaSell, AbuFactorBuyWD, AbuWeekMonthBuy, AbuDownUpTrend, AbuFactorSellNDay

from abupy import AbuKellyPosition

from abupy import AbuPickRegressAngMinMax, AbuPickStockPriceMinMax, AbuPickStockShiftDistance, AbuPickStockNTop

from abupy.UtilBu import ABuProgress

from abupy.CoreBu.ABu import run_loop_back

from base.models import Stock
from xadmin.plugins.actions import BaseActionView
from .models import Orders


class RunloopAction(BaseActionView):
    # 这里需要填写三个属性
    action_name = "change_sss"  #: 相当于这个 Action 的唯一标示, 尽量用比较针对性的名字
    description = u'回测 %(verbose_name_plural)s'  #: 描述, 出现在 Action 菜单中, 可以使用 ``%(verbose_name_plural)s`` 代替 Model 的名字.
    model_perm = 'change'
    console_info = []

    abupy.env.g_market_source = EMarketSourceType.E_MARKET_SOURCE_bd
    abupy.env.disable_example_env_ipython()

    lock = threading.Lock()
    console_str = []

    def print_to_str(self, s):
        self.console_info.append(s)
        print(s)

    def booth(self, obj):
        self.lock.acquire()

        if obj:
            self.console_info = []

            print('Thread_id', obj)

            stocks = obj.stocks.all()

            buy_factors = []
            sell_factors = []
            choice_symbols = []
            stock_pickers = []

            for factor_buy in obj.factor_buys.all():
                buy_obj = eval(factor_buy.class_name)
                buy_obj['position'] = AbuKellyPosition

                buy_factors.append(buy_obj)

            for factor_sell in obj.factor_sells.all():
                sell_factors.append(eval(factor_sell.class_name))

            for stock in stocks:
                choice_symbols.append(stock.symbol)

            for pick_stock in obj.pick_stocks.all():
                stock_pickers.append(eval(pick_stock.class_name))

            """ 
                8.1.4 对多支股票进行择时
                :return:
            """
            # sell_factor1 = eval("{'xd': 120, 'class': AbuFactorSellBreak}")
            # sell_factor2 = {'stop_loss_n': 0.5, 'stop_win_n': 3.0, 'class': AbuFactorAtrNStop}
            # sell_factor3 = {'class': AbuFactorPreAtrNStop, 'pre_atr_n': 1.0}
            # sell_factor4 = {'class': AbuFactorCloseAtrNStop, 'close_atr_n': 1.5}
            # sell_factors = [sell_factor1, sell_factor2, sell_factor3, sell_factor4]
            benchmark = AbuBenchmark(start=str(obj.start), end=str(obj.end))
            # buy_factors = [{'xd': 60, 'class': AbuFactorBuyBreak},
            #                {'xd': 42, 'class': AbuFactorBuyBreak}]

            # orders_pd, action_pd, all_fit_symbols_cnt = ABuPickTimeExecute.do_symbols_with_same_factors(choice_symbols,
            #                                                                                             benchmark,
            #                                                                                             buy_factors,
            #                                                                                             sell_factors,
            #                                                                                             capital,
            #                                                                                             show=False)

            abu_result_tuple, _ = run_loop_back(obj.read_cash,
                                                buy_factors,
                                                sell_factors,
                                                stock_pickers,
                                                choice_symbols=choice_symbols,
                                                start=str(obj.start),
                                                end=str(obj.end))
            if abu_result_tuple is None:
                return

            metrics = AbuMetricsBase(*abu_result_tuple, log=self.print_to_str)

            metrics.fit_metrics()

            orders_pd = abu_result_tuple.orders_pd

            if orders_pd is None:
                obj.status = 'done'
                obj.description = 'none'
                self.lock.release()
                return

            symbols = orders_pd['symbol'].unique()

            for symbol in symbols:
                stock = Stock.objects.get(symbol=symbol)

                print('stock', stock)

                orders_pd.loc[
                    orders_pd['symbol'] == ('%s' % stock.symbol), 'stock_id'] = stock.id

            orders_pd['run_loop_group_id'] = obj.id

            print('orders_pd', orders_pd.tail())

            for index, row in orders_pd.iterrows():
                dictObject = row.to_dict()
                Orders.objects.create(**dictObject)

            metrics.plot_returns_cmp(only_show_returns=True, only_info=True)

            # 其实我们做的只有这一部分 ********
            obj.status = 'done'
            obj.description = str(self.console_info)
            obj.save()
        else:
            print("Thread_id", obj, "No more")

        self.lock.release()

    def do_action(self, queryset):
        for obj in queryset:

            obj.status = 'run...'
            obj.description = 'run...'
            obj.save()

            orders = Orders.objects.filter(run_loop_group_id=obj.id)
            if len(orders) > 0:
                orders.delete()

            new_thread = threading.Thread(target=self.booth, args=(obj,))
            new_thread.start()

        # return HttpResponse('{"status": "success", "msg": "error"}', content_type='application/json')
