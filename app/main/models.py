from app import db
from app.models import Settlement

class Order(db.Model):

    OrderCode = db.Column(db.String(32),unique=True ,primary_key=True)
    TotalPrice = db.Column(db.Numeric(10, 2))
    Currency = db.Column(db.String(3))
    OrderState = db.Column(db.SmallInteger)
    TrackNumber = db.Column(db.String(256))

    source_id = db.Column(db.SmallInteger ,db.ForeignKey('source.SourceId'))
    client_id = db.Column(db.String(64) ,db.ForeignKey('customer.ClientUserAccount'))

    products = db.relationship('Product',backref='order',lazy='dynamic')
    tracks = db.relationship('Track',backref='order',lazy='dynamic')

class Product(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    SKU = db.Column(db.String(32))
    ProductsName = db.Column(db.String(32))
    ProductNum = db.Column(db.SmallInteger)
    ImgUrl = db.Column(db.String(128))

    order_id = db.Column(db.String(32),db.ForeignKey('order.OrderCode'))


class Source(db.Model):

    SourceId = db.Column(db.SmallInteger, primary_key=True)
    SourceName = db.Column(db.String(32))

    orders = db.relationship('Order',backref='source',lazy='dynamic')

class Customer(db.Model):

    ClientUserAccount = db.Column(db.String(64), primary_key=True)
    Email = db.Column(db.String(64))
    Telephone = db.Column(db.String(32))

    orders = db.relationship('Order',backref='customer',lazy='dynamic')

class Track(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    TrackNumber = db.Column(db.String(256))
    TrackId = db.Column(db.String(32))
    TrackName = db.Column(db.String(32))

    order_id = db.Column(db.String(32),db.ForeignKey('order.OrderCode'))

class TotalSettlement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Currency = db.Column(db.String(3))
    TotalPrice = db.Column(db.Numeric(10, 2))
    datetime= db.Column(db.Date)

class AMASettlement(Settlement):
    pass

class SMTSettlement(Settlement):
    pass

class EBASettlement(Settlement):
    pass

class WISSettlement(Settlement):
    pass

class OtherSettlement(Settlement):
    pass

class TypeSettlement(Settlement):
    pass

class SKUSettlement(Settlement):
    pass

class NumberSettlement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Account = db.Column(db.String(32))
    number = db.Column(db.Integer)
    datetime= db.Column(db.Date)

class SalesSettlement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Category = db.Column(db.String(32))
    OrderSourceName = db.Column(db.String(32))
    number = db.Column(db.Integer)
    Currency = db.Column(db.String(3))
    TotalPrice = db.Column(db.Numeric(10, 2))
    datetime= db.Column(db.Date)







