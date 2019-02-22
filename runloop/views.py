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
    orders = get_orders(id)
    symbol_ids = get_symbol_ids(orders)
    stock = Stock.objects.get(symbol=symbol_ids[0]),
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
        orders=json.dumps(get_order_map(orders)),
        symbol_ids=json.dumps(symbol_ids)
    )
    return HttpResponse(template.render(context, request))


# serializers.serialize("json", orders)

def get_orders(run_loop_group_id):
    orders = Orders.objects.filter(run_loop_group_id=run_loop_group_id)
    return orders


def get_order_map(orders):
    buy = []
    sell = []
    for order in orders:
        o = dict(
            buy_date=datetime.datetime.strptime(order.buy_date, '%Y%m%d').strftime('%Y-%m-%d'),
            buy_price=order.buy_price,
            buy_cnt=order.buy_cnt,
        )
        buy.append(o)
        o = dict(
            sell_date=datetime.datetime.strptime(order.sell_date, '%Y%m%d').strftime('%Y-%m-%d'),
            sell_price=order.sell_price,
            sell_cnt=order.buy_cnt,
        )
        sell.append(o)
    return dict(
        buy=buy,
        sell=sell
    )


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

    print("查询股票k", symbols, start)
    print("查询股票k", symbols, start, end)
    kls = ABuSymbolPd.make_kl_df(symbols, data_mode=EMarketDataSplitMode.E_DATA_SPLIT_SE, start=start,
                                 end=end, show_progress=True)
    print("查询股票k", symbols, kls)

    data = []
    for symbol in symbols:
        date_array = kls.major_axis.to_pydatetime()
        date_only_array = numpy.vectorize(lambda s: s.strftime('%Y-%m-%d'))(date_array)
        for date in date_only_array:
            data.append([
                date,
                kls[symbol, date, 'open'],
                kls[symbol, date, 'close'],
                kls[symbol, date, 'high'],
                kls[symbol, date, 'low']
            ])

    return data
