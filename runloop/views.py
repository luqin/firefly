from __future__ import unicode_literals

import json

import numpy
from django.core import serializers
from django.http import HttpResponse
from django.template import loader

from runloop.models import Orders
from runloop.models import RunLoopGroup


def index(request, id):
    template = loader.get_template('runloop/k.html')
    run_loop_group = RunLoopGroup.objects.get(id=id)
    orders = get_orders(id)
    symbols = get_symbols(orders)
    kls = get_kls(symbols)
    runloop_data = dict(
        # 数据意义：开盘(open)，收盘(close)，最低(lowest)，最高(highest)
        # TODO
        data=kls
    )
    context = dict(
        title='回测结果',
        run_loop_group=json.dumps(dict(
            name=run_loop_group.name
        )),
        runloopData=json.dumps(runloop_data),
        orders=serializers.serialize("json", orders),
        symbols=json.dumps(symbols)
    )
    return HttpResponse(template.render(context, request))


def get_orders(run_loop_group_id):
    orders = Orders.objects.filter(run_loop_group_id=run_loop_group_id)
    return orders


def get_symbols(orders):
    stocks = set()
    for order in orders:
        stocks.add(order.symbol)
    return list(stocks)


def get_kls(symbols):
    from abupy.MarketBu import ABuSymbolPd
    from abupy import EMarketDataSplitMode
    kls = ABuSymbolPd.make_kl_df(symbols, data_mode=EMarketDataSplitMode.E_DATA_SPLIT_SE, start='2018-02-18',
                                 end='2019-02-20', show_progress=True)
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
