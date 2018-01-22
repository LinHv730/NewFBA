from . import db

class BaseTable(db.Model): 
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True) 
    name = db.Column(db.String(64),unique=True)

class Settlement(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    Account = db.Column(db.String(32))
    Currency = db.Column(db.String(3))
    TotalPrice = db.Column(db.Numeric(10, 2))
    datetime= db.Column(db.Date)