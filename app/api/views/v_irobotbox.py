# -*- coding:utf-8 -*-

from app import db
from .. import irobotbox
from ..controller.c_irobotbox import GetIrobotboxOrder
from ..i18n import irobotbox_url, irobotbox_order_api
import datetime
# from app.order.models import OrderDetails, OrderProducts
from app.rate.models import Rates
from flask import redirect, url_for
from ..models.m_irobotbox import IrobotboxOrder as IBO, IrobotboxOrderProducts as IOP
from sqlalchemy import distinct


@irobotbox.route('/irobotboxorder')
def irobotboxorder():
    if int(datetime.datetime.now().strftime("%M")) < 10:
        Rates().get_rate()

    irobotbox_order_api['StartTime'] = (datetime.datetime.now()-datetime.timedelta(minutes=21)).strftime("%Y-%m-%d %H:%M:%S")
    irobotbox_order_api['EndTime'] = (datetime.datetime.now()-datetime.timedelta(minutes=10)).strftime("%Y-%m-%d %H:%M:%S")

    orders = GetIrobotboxOrder(url=irobotbox_url, key=irobotbox_order_api)
    result = orders.get_order()

    while result['NextToken'] != -1:
        orders = GetIrobotboxOrder(url=irobotbox_url, key=result)
        result = orders.get_order()


    return redirect(url_for('order.handling'))


@irobotbox.route('/skuisnull')
def skuIsNull():
    skus = db.session.query(distinct(IOP.order_id)).filter(IOP.SKU==None).all()

    nullskus =[]

    for sku in skus:
        irobotbox_order_api['OrderCode'] = sku[0]
        orders = GetIrobotboxOrder(url=irobotbox_url, key=irobotbox_order_api)
        result = orders.get_order()
        nullskus.append(sku[0])

    return str(nullskus)


@irobotbox.route('/irobotboxorders')
def irobotboxorders():

    irobotbox_order_api['StartTime'] = (datetime.datetime.now()-datetime.timedelta(hours=2)).strftime("%Y-%m-%d %H:%M:%S")
    irobotbox_order_api['EndTime'] = (datetime.datetime.now()-datetime.timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S")

    orders = GetIrobotboxOrder(url=irobotbox_url, key=irobotbox_order_api)
    result = orders.get_order()

    while result['NextToken'] != -1:
        orders = GetIrobotboxOrder(url=irobotbox_url, key=result)
        result = orders.get_order()

    return redirect(url_for('order.handling'))



