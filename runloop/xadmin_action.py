import os
import threading

import abupy
import numpy as np
from abupy import AbuFactorBuyBreak, AbuBenchmark, AbuCapital, ABuPickTimeExecute, AbuMetricsBase, AbuFactorAtrNStop, \
    AbuFactorCloseAtrNStop, \
    AbuFactorPreAtrNStop, AbuFactorSellBreak, ABuGridHelper, GridSearch, ABuFileUtil, WrsmScorer, EMarketSourceType
from base.models import Stock

from xadmin.plugins.actions import BaseActionView
from .models import Orders


class RunloopAction(BaseActionView):
    # 这里需要填写三个属性
    action_name = "change_sss"  #: 相当于这个 Action 的唯一标示, 尽量用比较针对性的名字
    description = u'回测 %(verbose_name_plural)s'  #: 描述, 出现在 Action 菜单中, 可以使用 ``%(verbose_name_plural)s`` 代替 Model 的名字.
    model_perm = 'change'
    console_info = []

    abupy.env.g_market_source = EMarketSourceType.E_MARKET_SOURCE_tx
    abupy.env.disable_example_env_ipython()

    lock = threading.Lock()
    console_str = []

    def print_to_str(self, s):
        self.console_info.append(s)
        print(s)

    def booth(self, obj):
        self.lock.acquire()

        if obj:
            print('Thread_id', obj)

            stocks = obj.stocks.all()

            buy_factors = []
            sell_factors = []
            choice_symbols = []

            for factor_buy in obj.factor_buys.all():
                buy_factors.append(eval(factor_buy.get_class_name_display()))

            for factor_sell in obj.factor_sells.all():
                sell_factors.append(eval(factor_sell.get_class_name_display()))

            for stock in stocks:
                choice_symbols.append(stock.symbol)

            """
                8.1.4 对多支股票进行择时
                :return:
            """
            # sell_factor1 = eval("{'xd': 120, 'class': AbuFactorSellBreak}")
            # sell_factor2 = {'stop_loss_n': 0.5, 'stop_win_n': 3.0, 'class': AbuFactorAtrNStop}
            # sell_factor3 = {'class': AbuFactorPreAtrNStop, 'pre_atr_n': 1.0}
            # sell_factor4 = {'class': AbuFactorCloseAtrNStop, 'close_atr_n': 1.5}
            # sell_factors = [sell_factor1, sell_factor2, sell_factor3, sell_factor4]
            benchmark = AbuBenchmark(start=obj.start, end=obj.end)
            # buy_factors = [{'xd': 60, 'class': AbuFactorBuyBreak},
            #                {'xd': 42, 'class': AbuFactorBuyBreak}]

            capital = AbuCapital(obj.read_cash, benchmark)
            orders_pd, action_pd, all_fit_symbols_cnt = ABuPickTimeExecute.do_symbols_with_same_factors(choice_symbols,
                                                                                                        benchmark,
                                                                                                        buy_factors,
                                                                                                        sell_factors,
                                                                                                        capital,
                                                                                                        show=False)

            metrics = AbuMetricsBase(orders_pd, action_pd, capital, benchmark, log=self.print_to_str)
            metrics.fit_metrics()

            if orders_pd is None:
                obj.status = 'done'
                obj.description = 'none'
                self.lock.release()
                return

            for stock in stocks:
                # stock = Stock.objects.filter(symbol=s.symbol)
                print(('%s%s' % (stock.market.lower(), stock.symbol)))
                orders_pd.loc[
                    orders_pd['symbol'] == ('%s%s' % (stock.market.lower(), stock.symbol)), 'stock_id'] = stock.id

            orders_pd['run_loop_group_id'] = obj.id

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


class GridSearchAction(BaseActionView):
    action_name = "change_grid_search"  #: 相当于这个 Action 的唯一标示, 尽量用比较针对性的名字
    description = u'Grid Search 最优参数 %(verbose_name_plural)s'  #: 描述, 出现在 Action 菜单中, 可以使用 ``%(verbose_name_plural)s`` 代替 Model 的名字.
    model_perm = 'change'

    def gen_factor_params(self, show=True):
        """
        参数进行排列组合
        :return:
        """

        xd_sell_range = np.arange(10, 20, 3)
        xd_buy_range = np.arange(5, 10, 3)

        sell_bk_factor_grid = {
            'class': [AbuFactorSellBreak],
            'xd': xd_sell_range
        }

        sell_factors_product = ABuGridHelper.gen_factor_grid(
            ABuGridHelper.K_GEN_FACTOR_PARAMS_SELL,
            [sell_bk_factor_grid])

        if show:
            print('卖出因子参数共有{}种组合方式'.format(len(sell_factors_product)))
            print('卖出因子组合0形式为{}'.format(sell_factors_product[0]))

        buy_bk_factor_grid = {
            'class': [AbuFactorBuyBreak],
            'xd': xd_buy_range
        }

        buy_factors_product = ABuGridHelper.gen_factor_grid(
            ABuGridHelper.K_GEN_FACTOR_PARAMS_BUY, [buy_bk_factor_grid])

        if show:
            print('买入因子参数共有{}种组合方式'.format(len(buy_factors_product)))
            print('买入因子组合形式为{}'.format(buy_factors_product))

        return sell_factors_product, buy_factors_product

    def do_action(self, queryset):
        for obj in queryset:
            print('GridSearchAction')
            score_fn = '../gen/score_tuple_array'

            read_cash = obj.read_cash
            stocks = obj.stocks.all()

            choice_symbols = []
            for stock in stocks:
                choice_symbols.append(stock.symbol)

            sell_factors_product, buy_factors_product = self.gen_factor_params(True)

            grid_search = GridSearch(read_cash, choice_symbols,
                                     buy_factors_product=buy_factors_product,
                                     sell_factors_product=sell_factors_product)

            if not ABuFileUtil.file_exist(score_fn):
                """
                    注意下面的运行耗时大约1小时多，如果所有cpu都用上的话，也可以设置n_jobs为 < cpu进程数，一边做其它的一边跑
                """
                # 运行GridSearch n_jobs=-1启动cpu个数的进程数
                scores, score_tuple_array = grid_search.fit(n_jobs=-1)

                """  
                    针对运行完成输出的score_tuple_array可以使用dump_pickle保存在本地，以方便修改其它验证效果。
                """
                ABuFileUtil.dump_pickle(score_tuple_array, score_fn)

                print('组合因子参数数量{}'.format(len(buy_factors_product) * len(sell_factors_product)))
                print('最终评分结果数量{}'.format(len(scores)))

            else:
                """
                    直接读取本地序列化文件
                """
                score_tuple_array = ABuFileUtil.load_pickle(score_fn)

                # 实例化一个评分类WrsmScorer，它的参数为之前GridSearch返回的score_tuple_array对象
                scorer = WrsmScorer(score_tuple_array)
                print('scorer.score_pd.tail():\n', scorer.score_pd.tail())

                # score_tuple_array[658]与grid_search.best_score_tuple_grid是一致的
                scorer_returns_max = scorer.fit_score()

                # 因为是倒序排序，所以index最后一个为最优参数
                best_score_tuple_grid = score_tuple_array[scorer_returns_max.index[-1]]
                # 由于篇幅，最优结果只打印文字信息
                AbuMetricsBase.show_general(best_score_tuple_grid.orders_pd,
                                            best_score_tuple_grid.action_pd,
                                            best_score_tuple_grid.capital,
                                            best_score_tuple_grid.benchmark,
                                            only_info=True)

                # 最后打印出只考虑投资回报下最优结果使用的买入策略和卖出策略
                print('best_score_tuple_grid.buy_factors, best_score_tuple_grid.sell_factors:\n',
                      best_score_tuple_grid.buy_factors,
                      best_score_tuple_grid.sell_factors)

                obj.description = 'best_score_tuple_grid.buy_factors:%s, best_score_tuple_grid.sell_factors:%s' % (
                    best_score_tuple_grid.buy_factors,
                    best_score_tuple_grid.sell_factors)
                obj.save()
