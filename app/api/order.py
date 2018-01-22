from app.api.i18n.zh_CN import irobotbox_url, irobotbox_order_api
import datetime
from app.api.controller.c_irobotbox import GetIrobotboxOrder

def get_order_all(x, y):

    irobotbox_order_api['StartTime'] = (datetime.datetime.now()-datetime.timedelta(days=x)).strftime("%Y-%m-%d %H:%M:%S")
    irobotbox_order_api['EndTime'] = (datetime.datetime.now()-datetime.timedelta(days=y)).strftime("%Y-%m-%d %H:%M:%S")

    orders = GetIrobotboxOrder(url=irobotbox_url, key=irobotbox_order_api)
    result = orders.get_order()

    while result['NextToken'] != -1:
        orders = GetIrobotboxOrder(url=irobotbox_url, key=result)
        result = orders.get_order()
        print(result['NextToken'])