import os
import threading

import abupy
import numpy as np
from abupy import AbuFactorBuyBreak, AbuBenchmark, AbuCapital, ABuPickTimeExecute, AbuMetricsBase, AbuFactorAtrNStop, \
    AbuFactorCloseAtrNStop, \
    AbuFactorPreAtrNStop, AbuFactorSellBreak, ABuGridHelper, GridSearch, ABuFileUtil, WrsmScorer, EMarketSourceType
from base.models import Stock

from xadmin.plugins.actions import BaseActionView


class GridSearchAction(BaseActionView):
    action_name = "change_grid_search"  #: 相当于这个 Action 的唯一标示, 尽量用比较针对性的名字
    description = u'Grid Search 最优参数 %(verbose_name_plural)s'  #: 描述, 出现在 Action 菜单中, 可以使用 ``%(verbose_name_plural)s`` 代替 Model 的名字.
    model_perm = 'change'

    lock = threading.Lock()
    console_str = []

    def booth(self, obj, score_fn):
        self.lock.acquire()

        if obj:
            print('Thread_id', obj)
            benchmark = AbuBenchmark(start=str(obj.start), end=str(obj.end))

            read_cash = obj.read_cash
            stocks = obj.stocks.all()

            choice_symbols = []
            for stock in stocks:
                choice_symbols.append(stock.symbol)

            sell_factors_product, buy_factors_product = self.gen_factor_params(obj, True)

            grid_search = GridSearch(read_cash, choice_symbols, benchmark=benchmark,
                                     buy_factors_product=buy_factors_product,
                                     sell_factors_product=sell_factors_product)

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
            print("Thread_id", obj, "No more")

        self.lock.release()

    def gen_factor_params(self, obj, show=True):
        """
        参数进行排列组合
        :return:
        """

        buy_factors = []
        sell_factors = []

        for factor_buy in obj.factor_buys.all():
            buy_factors.append(eval(factor_buy.get_class_name_display()))

        for factor_sell in obj.factor_sells.all():
            sell_factors.append(eval(factor_sell.get_class_name_display()))

        sell_factors_product = ABuGridHelper.gen_factor_grid(
            ABuGridHelper.K_GEN_FACTOR_PARAMS_SELL,
            sell_factors)

        if show:
            print('卖出因子参数共有{}种组合方式'.format(len(sell_factors_product)))
            print('卖出因子组合0形式为{}'.format(sell_factors_product[0]))

        buy_factors_product = ABuGridHelper.gen_factor_grid(
            ABuGridHelper.K_GEN_FACTOR_PARAMS_BUY, buy_factors)

        if show:
            print('买入因子参数共有{}种组合方式'.format(len(buy_factors_product)))
            print('买入因子组合形式为{}'.format(buy_factors_product))

        return sell_factors_product, buy_factors_product

    def do_action(self, queryset):
        for obj in queryset:

            print('GridSearchAction')
            score_fn = '../gen/score_tuple_array_%s' % str(obj.id)

            if not ABuFileUtil.file_exist(score_fn):

                new_thread = threading.Thread(target=self.booth, args=(obj,score_fn, ))
                new_thread.start()

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
