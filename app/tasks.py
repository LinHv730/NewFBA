from extensions import celery
# from suds.client import Client
import datetime
from app.api.models.m_irobotbox import Log
from app.api.views.v_irobotbox import irobotboxorder
from app.api.controller.c_irobotbox import GetIrobotboxOrder
from app.api.i18n import irobotbox_url, irobotbox_order_api
from app.rate.models import Rates
from app import db
@celery.task()
def getIrobotboxorder():
    if int(datetime.datetime.now().strftime("%M")) < 10:
        Rates().get_rate()

    irobotbox_order_api['StartTime'] = (datetime.datetime.now()-datetime.timedelta(minutes=60)).strftime("%Y-%m-%d %H:%M:%S")
    irobotbox_order_api['EndTime'] = (datetime.datetime.now()-datetime.timedelta(minutes=10)).strftime("%Y-%m-%d %H:%M:%S")

    orders = GetIrobotboxOrder(url=irobotbox_url, key=irobotbox_order_api)
    result = orders.get_order()
    orders.save_info()
    flag_arr=[]
    flag_arr.append(result['NextToken'])

    while result['NextToken'] != -1:
        orders = GetIrobotboxOrder(url=irobotbox_url, key=result)
        result = orders.get_order()
        flag_arr.append(result['NextToken'])

    if -1 not in flag_arr:
        flag=0
    else:
        flag=1

    log=Log(start_time=irobotbox_order_api['StartTime'],end_time=irobotbox_order_api['EndTime'],state=flag)
    db.session.add(log)

    return '数据抓取成功'

@celery.task()
def getdataAgain():
    logs = Log.query.filter_by(state=0).all()
    if len(logs) != 0:
        for notlog in logs:
            irobotbox_order_api['StartTime'] = notlog.start_time
            irobotbox_order_api['EndTime'] = notlog.end_time

            orders = GetIrobotboxOrder(url=irobotbox_url, key=irobotbox_order_api)
            result = orders.get_order()
            flag_arr=[]
            flag_arr.append(result['NextToken'])

            while result['NextToken'] != -1:
                orders = GetIrobotboxOrder(url=irobotbox_url, key=result)
                result = orders.get_order()
                flag_arr.append(result['NextToken'])

            if -1 not in flag_arr:
                flag=0
            else:
                flag=1

        notlog.state=flag
        db.session.add(notlog)

    return '数据补抓取成功'
