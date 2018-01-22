# -*- coding:utf-8 -*-

from app import db
from datetime import datetime
import re, urllib.request

class Rates(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    currency = db.Column(db.String(3))
    rate = db.Column(db.Numeric(10, 5))
    trade_time = db.Column(db.DateTime)

    def get_rate(self):
        currencys = ['EUR', 'USD', 'GBP', 'JPY', 'CAD', 'MXN', 'AUD']
        trade_time = datetime.now()
        for currency in currencys:
            url = 'http://hl.anseo.cn/cal_{currency}_To_CNY_1.aspx'.format(currency=currency)
            response = urllib.request.urlopen(url)
            html = response.read().decode('utf-8')

            rates_re = re.compile(r'<p><strong>当前汇率：</strong>(.*?)</p>')
            result = rates_re.findall(html)

            if result[0]:
                rate = Rates(currency=currency, rate=float(result[0]), trade_time=trade_time)
                db.session.add(rate)
                db.session.commit()

    def last_rate(self):
        results = Rates.query.order_by(Rates.trade_time.desc()).limit(12).all()
        tormb = {}

        for result in results:
            tormb[result.currency] = result.rate

            if len(tormb) == 7:
                break

        return tormb






