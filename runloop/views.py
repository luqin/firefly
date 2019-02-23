from __future__ import unicode_literals

import datetime
import json

import numpy
from django.http import HttpResponse
from django.template import loader

from base.models import Stock
from .models import Orders
from .models import RunLoopGroup


def index(request, id):
    template = loader.get_template('runloop/k.html')
    run_loop_group = RunLoopGroup.objects.get(id=id)
    orders = Orders.objects.filter(run_loop_group_id=id)
    symbol_ids = get_symbol_ids(orders)
    stock = Stock.objects.get(symbol=symbol_ids[0])
    k_data = get_k_data(symbol_ids, run_loop_group)
    context = dict(
        run_loop_group=run_loop_group,
        run_loop_group_json=json.dumps(dict(
            name=run_loop_group.name,
            status=run_loop_group.status,
            start=run_loop_group.start.__format__("%Y-%m-%d"),
            end=run_loop_group.end.__format__("%Y-%m-%d"),
        )),
        stock=stock,
        k_data=json.dumps(k_data),
        orders=json.dumps(get_orders(orders)),
        symbol_ids=json.dumps(symbol_ids)
    )
    return HttpResponse(template.render(context, request))


# serializers.serialize("json", orders)


def get_orders(orders):
    new_orders = []

    for order in orders:
        o = dict(
            buy_date=datetime.datetime.strptime(order.buy_date, '%Y%m%d').strftime('%Y-%m-%d'),
            buy_price=order.buy_price,
            buy_cnt=order.buy_cnt,
            buy_factor=order.buy_factor,
            symbol=order.symbol,
            buy_pos=order.buy_pos,
            buy_type_str=order.buy_type_str,
            expect_direction=order.expect_direction,
            sell_type_extra=order.sell_type_extra,
            sell_date=datetime.datetime.strptime(order.sell_date, '%Y%m%d').strftime(
                '%Y-%m-%d') if (order.sell_date and order.sell_date != '0') else order.sell_date,
            sell_price=order.sell_price,
            sell_type=order.sell_type,
            ml_features=order.ml_features,
            key=order.key,
            profit=order.profit,
            result=order.result,
            profit_cg=order.profit_cg,
            profit_cg_hunder=order.profit_cg_hunder,
            keep_days=order.keep_days,
        )
        new_orders.append(o)

    return new_orders


# o.buy_date.__format__("%Y-%m-%d")


def get_symbol_ids(orders):
    stocks = set()
    for order in orders:
        stocks.add(order.symbol)
    print('股票：', stocks)
    return list(stocks)


# 数据意义：开盘(open)，收盘(close)，最低(lowest)，最高(highest)
def get_k_data(symbols, run_loop_group):
    from abupy.MarketBu import ABuSymbolPd
    from abupy import EMarketDataSplitMode

    start = run_loop_group.start.strftime("%Y-%m-%d")
    end = run_loop_group.end.strftime("%Y-%m-%d")

    kline = ABuSymbolPd.make_kl_df(symbols, data_mode=EMarketDataSplitMode.E_DATA_SPLIT_SE, start=start,
                                   end=end, show_progress=True)
    print("查询股票kline data", symbols, kline)

    data = []
    for symbol in symbols:
        date_array = kline.major_axis.to_pydatetime()
        date_only_array = numpy.vectorize(lambda s: s.strftime('%Y-%m-%d'))(date_array)
        for date in date_only_array:
            data.append([
                date,
                kline[symbol, date, 'open'],
                kline[symbol, date, 'close'],
                kline[symbol, date, 'high'],
                kline[symbol, date, 'low']
            ])

    return data
