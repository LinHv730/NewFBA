# -*- coding:utf-8 -*-

from . import rate
from .models import Rates

@rate.route('/MXN')
def mxn():
    url = 'http://hl.anseo.cn/cal_MXN_To_CNY_1.aspx'
    response = urllib.request.urlopen(url)
    html = response.read().decode('utf-8')

    rates_re = re.compile(r'<p><strong>当前汇率：</strong>(.*?)</p>')
    result = rates_re.findall(html)

    return str(result)


@rate.route('/exchange')
def exchange():
    rate = Rates()
    rate.get_rate()
    return "添加成功"