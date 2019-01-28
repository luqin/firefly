from django.test import TestCase

# Create your tests here.
from abuui.abupy import AbuFactorBuyBreak,AbuBenchmark, AbuCapital, AbuKLManager, AbuPickTimeWorker, ABuTradeProxy, ABuTradeExecute

import matplotlib.pyplot as plt


class AbuTest(TestCase):
    
    def test_simple(self):
        """
            8.1.1 买入因子的实现
            :return:
            """
        # buy_factors 60日向上突破，42日向上突破两个因子
        buy_factors = [{'xd': 60, 'class': AbuFactorBuyBreak},
                       {'xd': 42, 'class': AbuFactorBuyBreak}]
        benchmark = AbuBenchmark()
        capital = AbuCapital(1000000, benchmark)
        kl_pd_manager = AbuKLManager(benchmark, capital)
        # 获取TSLA的交易数据
        kl_pd = kl_pd_manager.get_pick_time_kl_pd('usTSLA')
        abu_worker = AbuPickTimeWorker(capital, kl_pd, benchmark, buy_factors, None)
        abu_worker.fit()

        orders_pd, action_pd, _ = ABuTradeProxy.trade_summary(abu_worker.orders, kl_pd, draw=True)

        ABuTradeExecute.apply_action_to_capital(capital, action_pd, kl_pd_manager)
        capital.capital_pd.capital_blance.plot()
        plt.show()