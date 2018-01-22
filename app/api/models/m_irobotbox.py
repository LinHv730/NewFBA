# -*- coding:utf-8 -*-

from app import db

class IrobotboxOrder(db.Model):
    __tablename__ = 'irobotbox_orders'
    OrderCode = db.Column(db.String(32), primary_key=True)
    ClientOrderCode = db.Column(db.String(32))
    SalesRecordNumber = db.Column(db.Integer)
    TransactionId = db.Column(db.String(32))
    ClientUserAccount = db.Column(db.String(64))
    Email = db.Column(db.String(64))
    Telephone = db.Column(db.String(32))
    OrderSourceID = db.Column(db.SmallInteger)
    OrderSourceName = db.Column(db.String(32))
    IsPay = db.Column(db.Boolean)
    PaymentMethods = db.Column(db.String(32))
    OrderStatus = db.Column(db.SmallInteger)
    OrderState = db.Column(db.SmallInteger)
    PayTime = db.Column(db.DateTime)
    Currency = db.Column(db.String(3))
    TotalPrice = db.Column(db.Numeric(10, 2))
    PromotionDiscountAmount = db.Column(db.Numeric(10, 2))
    TransportPay = db.Column(db.Numeric(10, 2))
    Country = db.Column(db.String(2))
    TransportID = db.Column(db.SmallInteger)
    IsFBAOrder = db.Column(db.Boolean)
    WareHouseID = db.Column(db.SmallInteger)    
    ProductWeight = db.Column(db.Numeric(10, 2))
    ShipService = db.Column(db.String(64))
    TrackNumbers = db.Column(db.String(256))
    PaypalFee = db.Column(db.Numeric(10, 2))
    RefundPaypalFee = db.Column(db.Numeric(10, 2))
    PaypalTransactionFee = db.Column(db.Numeric(10, 2))

    Oper1 = db.Column(db.Boolean)
    Oper2 = db.Column(db.Boolean)
    Oper3 = db.Column(db.Boolean)
    Oper4 = db.Column(db.Boolean)
    Oper5 = db.Column(db.Boolean)


    orderproducts = db.relationship('IrobotboxOrderProducts', backref='irobotbox_orders', lazy='dynamic')

    def __init__(self, ordercode=None):
        self.ordercode = ordercode


    def order_exist(self):
        if IrobotboxOrder.query.get(self.ordercode):
            return IrobotboxOrder.query.get(self.ordercode)
        else:
            return False



class IrobotboxOrderProducts(db.Model):
    __tablename__ = 'irobotbox_order_products'
    id = db.Column(db.Integer, primary_key=True)
    SKU = db.Column(db.String(32))
    ClientSKU = db.Column(db.String(32))
    GroupSKU = db.Column(db.String(32))
    GroupProductNum = db.Column(db.SmallInteger)
    GroupProductPrice = db.Column(db.Numeric(10, 2))
    ProductNum = db.Column(db.SmallInteger)
    ProductPrice = db.Column(db.Numeric(10, 2))
    ShippingPrice = db.Column(db.Numeric(10, 2))
    LastBuyPrice = db.Column(db.Numeric(10, 2))
    LastSupplierPrice = db.Column(db.Numeric(10, 2))
    FirstLegFee = db.Column(db.Numeric(10, 2))
    TariffFee = db.Column(db.Numeric(10, 2))
    SellerSKU = db.Column(db.String(64))
    OrderItemId = db.Column(db.String(64))
    ASIN = db.Column(db.String(64))
    ParameterValues = db.Column(db.String(256))
    IsBuildPackage = db.Column(db.Boolean)
    ProductWeight = db.Column(db.Numeric(10, 2))
    ProductLength = db.Column(db.Numeric(10, 2))
    ProductWidth = db.Column(db.Numeric(10, 2))
    ProductHeight = db.Column(db.Numeric(10, 2))
    BusinessAdminID = db.Column(db.SmallInteger)
    ProductLinks = db.Column(db.String(256))
    ProductLatestCost = db.Column(db.Numeric(10, 2))
    NetWeight = db.Column(db.Numeric(10, 2))
    ItemTax = db.Column(db.Numeric(10, 2))

    order_id = db.Column(db.String(19), db.ForeignKey('irobotbox_orders.OrderCode'))


class Log(db.Model):
    __tablename__ = 'logs'
    id = db.Column(db.Integer, primary_key=True) 
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    state = db.Column(db.Boolean)