# -*- coding:utf-8 -*-

from suds.client import Client
from ..models.m_irobotbox import IrobotboxOrder, IrobotboxOrderProducts
from app.main.models import Order,Product,Source,Customer,Track,TotalSettlement,AMASettlement,\
SMTSettlement,EBASettlement,WISSettlement,OtherSettlement,TypeSettlement,SKUSettlement,\
NumberSettlement,SalesSettlement
from app import db
from sqlalchemy import or_
import datetime

class GetIrobotboxOrder(object):
    def __init__(self, url, key):
        self.url = url
        self.key = key

    def get_order(self):
        client = Client(self.url)
        results = client.service.GetOrders(self.key)
        orders = results.OrderInfoList.ApiOrderInfo

        for i in range(len(orders)):
            order = IrobotboxOrder(ordercode=orders[i].OrderCode)

            check_order = order.order_exist()
            startime = (datetime.datetime.now()-datetime.timedelta(days=5)).strftime("%Y-%m-%d %H:%M:%S")

            if check_order:
                check_order.OrderStatus = orders[i].OrderStatus
                check_order.OrderState = orders[i].OrderState
                check_order.TransportID = orders[i].TransportID
                check_order.WareHouseID = orders[i].WareHouseID
                check_order.TrackNumbers = orders[i].TrackNumbers

                records = IrobotboxOrderProducts.query.filter_by(order_id=orders[i].OrderCode).all()
                products = results.OrderInfoList.ApiOrderInfo[i].OrderList.ApiOrderList

                for record in records:
                    if record.SKU == None:
                        for product in products:
                            if product.SellerSKU == record.SellerSKU:
                                record.SKU = product.SKU
                                record.ClientSKU = product.ClientSKU.encode("UTF-8") if product.ClientSKU else None
                                record.GroupSKU = product.GroupSKU.encode("UTF-8") if product.GroupSKU else None
                                record.GroupProductNum = product.GroupProductNum
                                record.GroupProductPrice = product.GroupProductPrice
                                record.ProductNum = product.ProductNum
                                record.ProductPrice = product.ProductPrice
                                record.ShippingPrice = product.ShippingPrice
                                record.LastBuyPrice = product.LastBuyPrice
                                record.LastSupplierPrice = product.LastSupplierPrice
                                record.FirstLegFee = product.FirstLegFee
                                record.TariffFee = product.TariffFee
                                record.IsBuildPackage = product.IsBuildPackage
                                record.ProductWeight = product.ProductWeight
                                record.ProductLength = product.ProductLength
                                record.ProductWidth = product.ProductWidth
                                record.ProductHeight = product.ProductHeight
                                record.BusinessAdminID = product.BusinessAdminID
                                record.ProductLinks = product.ProductLinks.encode("UTF-8") if product.ProductLinks else None
                                record.ProductLatestCost = product.ProductLatestCost



                db.session.add(check_order)
                db.session.commit()

            elif len(results.OrderInfoList.ApiOrderInfo[i].OrderList) and orders[i].IsPay and orders[i].TotalPrice > 0 and orders[i].OrderStatus != 2:
                order.OrderCode = orders[i].OrderCode
                order.ClientOrderCode = orders[i].ClientOrderCode.encode("UTF-8") if orders[i].ClientOrderCode else None
                order.SalesRecordNumber = orders[i].SalesRecordNumber
                order.TransactionId = orders[i].TransactionId
                order.ClientUserAccount = orders[i].ClientUserAccount
                order.Email = orders[i].Email
                order.Telephone = orders[i].Telephone
                order.OrderSourceID = orders[i].OrderSourceID
                order.OrderSourceName = orders[i].OrderSourceName.encode("UTF-8") if orders[i].OrderSourceName else None
                order.IsPay = orders[i].IsPay
                order.PaymentMethods = orders[i].PaymentMethods
                order.OrderStatus = orders[i].OrderStatus
                order.OrderState = orders[i].OrderState
                order.PayTime = orders[i].PayTime
                order.Currency = orders[i].Currency
                order.TotalPrice = orders[i].TotalPrice
                order.PromotionDiscountAmount = orders[i].PromotionDiscountAmount
                order.TransportPay = orders[i].TransportPay
                order.Country = orders[i].Country
                order.TransportID = orders[i].TransportID
                order.IsFBAOrder = orders[i].IsFBAOrder
                order.WareHouseID = orders[i].WareHouseID
                order.ProductWeight = orders[i].ProductWeight
                order.TrackNumbers = orders[i].TrackNumbers
                order.PaypalFee = orders[i].PaypalFee
                order.RefundPaypalFee = orders[i].RefundPaypalFee
                order.PaypalTransactionFee = orders[i].PaypalTransactionFee

                order.orderproducts = []

                products = results.OrderInfoList.ApiOrderInfo[i].OrderList.ApiOrderList

                for j in range(len(products)):
                    product = IrobotboxOrderProducts()
                    product.SKU = products[j].SKU
                    product.ClientSKU = products[j].ClientSKU.encode("UTF-8") if products[j].ClientSKU else None
                    product.GroupSKU = products[j].GroupSKU.encode("UTF-8") if products[j].GroupSKU else None
                    product.GroupProductNum = products[j].GroupProductNum
                    product.GroupProductPrice = products[j].GroupProductPrice
                    product.ProductNum = products[j].ProductNum
                    product.ProductPrice = products[j].ProductPrice
                    product.ShippingPrice = products[j].ShippingPrice
                    product.LastBuyPrice = products[j].LastBuyPrice
                    product.LastSupplierPrice = products[j].LastSupplierPrice
                    product.FirstLegFee = products[j].FirstLegFee
                    product.TariffFee = products[j].TariffFee
                    product.SellerSKU = products[j].SellerSKU
                    product.OrderItemId = products[j].OrderItemId
                    product.ASIN = products[j].ASIN
                    product.ParameterValues = products[j].ParameterValues.encode("UTF-8") if products[j].ParameterValues else None
                    product.IsBuildPackage = products[j].IsBuildPackage
                    product.ProductWeight = products[j].ProductWeight
                    product.ProductLength = products[j].ProductLength
                    product.ProductWidth = products[j].ProductWidth
                    product.ProductHeight = products[j].ProductHeight
                    product.BusinessAdminID = products[j].BusinessAdminID
                    product.ProductLinks = products[j].ProductLinks.encode("UTF-8") if products[j].ProductLinks else None
                    product.ProductLatestCost = products[j].ProductLatestCost
                    product.NetWeight = products[j].NetWeight
                    product.ItemTax = products[j].ItemTax

                    order.orderproducts.append(product)

                db.session.add(order)
                db.session.commit()


        self.key['NextToken'] = results.NextToken
        return self.key



    def save_info(self):

        irobotboxs = IrobotboxOrder.query.filter_by( Oper1 = None ).all()

        ####获取所有渠道
        for ib in irobotboxs:
            check_source = Source.query.filter_by(SourceId = ib.OrderSourceID).first()
            if check_source:
                pass
            else:
                source = Source(SourceId = ib.OrderSourceID, SourceName = ib.OrderSourceName)
                db.session.add(source)
                db.session.commit()

            check_customer = Customer.query.filter_by(ClientUserAccount = ib.ClientUserAccount).first()
            if check_customer:
                pass
            else:
                customer = Customer(ClientUserAccount = ib.ClientUserAccount,Email=ib.Email,Telephone=ib.Telephone)
                db.session.add(customer)
                db.session.commit()

            order = Order(OrderCode = ib.OrderCode, Currency = ib.Currency,TrackNumber=ib.TrackNumbers,\
             TotalPrice = ib.TotalPrice)
            track = Track(TrackNumber=ib.TrackNumbers,order_id=ib.OrderCode)
            order.source_id = ib.OrderSourceID
            order.client_id = ib.ClientUserAccount
            db.session.add(order)
            db.session.add(track)
            ib.Oper1 = 1

            gettotalSettlement(ib.OrderCode,ib.TotalPrice,ib.Currency,'total',TotalSettlement)

            chanel = ib.OrderSourceName

            gettotalSettlement(ib.OrderCode,ib.TotalPrice,ib.Currency,chanel,TypeSettlement)
            
            sourcename = chanel[:3]

            if sourcename=='Ama':

                gettotalSettlement(ib.OrderCode,ib.TotalPrice,ib.Currency,'AMA',AMASettlement)

            elif sourcename=='SMT':

                gettotalSettlement(ib.OrderCode,ib.TotalPrice,ib.Currency,'SMT',SMTSettlement)

            elif sourcename=='eba':

                gettotalSettlement(ib.OrderCode,ib.TotalPrice,ib.Currency,'EBA',EBASettlement)

            elif sourcename=='WIS':

                gettotalSettlement(ib.OrderCode,ib.TotalPrice,ib.Currency,'WIS',WISSettlement)

            else:
                gettotalSettlement(ib.OrderCode,ib.TotalPrice,ib.Currency,'other',OtherSettlement)

            
            
        irobotboxsproduct = IrobotboxOrderProducts.query.all()

        for ibp in irobotboxsproduct:    
            product = Product(SKU = ibp.SKU, ProductNum = ibp.ProductNum, order_id = ibp.order_id)
            db.session.add(product)
            db.session.commit()

            getskuSettlement(ibp.order_id,ibp.SKU,SKUSettlement)

            getnumSettlement(ibp.order_id,ibp.SKU,ibp.ProductNum,NumberSettlement)

            getsaleSettlement(ibp.order_id,ibp.ClientSKU,ibp.ProductNum,SalesSettlement)
            


def gettotalSettlement(OrderCodes,TotalPrices,Currencys,chanels,tabelname):
    todaytime = datetime.datetime.now().strftime("%Y-%m-%d")
    Strtoday = datetime.datetime.now().strftime("%Y%m%d")
    Strorder= OrderCodes[:8]
    ordertime=Strorder[:4]+'-'+Strorder[4:6]+'-'+Strorder[-2:]
    if chanels=='total':
        if Strtoday==Strorder:
            check_currency = tabelname.query.filter_by(datetime = todaytime,Currency=Currencys).first()
            if check_currency:
                check_currency.TotalPrice+=TotalPrices
                db.session.add(check_currency)
            else:
                totalset = tabelname(Currency=Currencys,datetime = todaytime,\
                    TotalPrice = TotalPrices)
                db.session.add(totalset)
        else:
            check_currency = tabelname.query.filter_by(datetime = ordertime,Currency=Currencys).first()
            if check_currency:
                check_currency.TotalPrice+=TotalPrices
                db.session.add(check_currency)
            else:
                totalset = tabelname(Currency=Currencys,datetime = ordertime,\
                    TotalPrice = TotalPrices)
                db.session.add(totalset)

    else:
        if Strtoday==Strorder:
            check_currency = tabelname.query.filter_by(Account=chanels,datetime = todaytime,Currency=Currencys).first()
            if check_currency:
                check_currency.TotalPrice+=TotalPrices
                db.session.add(check_currency)
            else:
                totalset = tabelname(Account=chanels,Currency=Currencys,datetime = todaytime,\
                    TotalPrice = TotalPrices)
                db.session.add(totalset)
        else:
            check_currency = tabelname.query.filter_by(Account=chanels,datetime = ordertime,Currency=Currencys).first()
            if check_currency:
                check_currency.TotalPrice+=TotalPrices
                db.session.add(check_currency)
            else:
                totalset = tabelname(Account=chanels,Currency=Currencys,datetime = ordertime,\
                    TotalPrice = TotalPrices)
                db.session.add(totalset)

def getskuSettlement(OrderCodes,SKUS,tabelname):
    irobotboxs1 = IrobotboxOrder.query.filter_by( OrderCode = OrderCodes).first()
    todaytime = datetime.datetime.now().strftime("%Y-%m-%d")
    Strtoday = datetime.datetime.now().strftime("%Y%m%d")
    Strorder= OrderCodes[:8]
    ordertime=Strorder[:4]+'-'+Strorder[4:6]+'-'+Strorder[-2:]
    if Strtoday==Strorder:
        check_currency = tabelname.query.filter_by(Account=SKUS,datetime = todaytime,\
            Currency=irobotboxs1.Currency).first()

        if check_currency:
            check_currency.TotalPrice=irobotboxs1.TotalPrice
            db.session.add(check_currency)
        else:
            totalset = tabelname(Account=SKUS,Currency=irobotboxs1.Currency,datetime = todaytime,\
            TotalPrice = irobotboxs1.TotalPrice)
            db.session.add(totalset)
    else:
        check_currency = tabelname.query.filter_by(Account=SKUS,datetime = ordertime,\
            Currency=irobotboxs1.Currency).first()
        if check_currency:
            check_currency.TotalPrice=irobotboxs1.TotalPrice
            db.session.add(check_currency)
        else:
            totalset = tabelname(Account=SKUS,Currency=irobotboxs1.Currency,datetime = ordertime,\
                TotalPrice = irobotboxs1.TotalPrice)
            db.session.add(totalset)

def getnumSettlement(OrderCodes,SKUS,ProductNums,tabelname):
    todaytime = datetime.datetime.now().strftime("%Y-%m-%d")
    Strtoday = datetime.datetime.now().strftime("%Y%m%d")
    Strorder= OrderCodes[:8]
    ordertime=Strorder[:4]+'-'+Strorder[4:6]+'-'+Strorder[-2:]

    if Strtoday==Strorder:
        check_currency = tabelname.query.filter_by(Account=SKUS,datetime = todaytime).first()

        if check_currency:
            check_currency.number=ProductNums
            db.session.add(check_currency)
        else:
            totalset = tabelname(Account=SKUS,number=ProductNums,datetime = todaytime)
            db.session.add(totalset)
    else:
        check_currency = tabelname.query.filter_by(Account=SKUS,datetime = ordertime).first()
        if check_currency:
            check_currency.number=ProductNums
            db.session.add(check_currency)
        else:
            totalset = tabelname(Account=SKUS,number=ProductNums,datetime = ordertime)
            db.session.add(totalset)

def getsaleSettlement(OrderCodes,CLSKUS,ProductNums,tabelname):
    irobotboxs1 = IrobotboxOrder.query.filter_by( OrderCode = OrderCodes).first()
    todaytime = datetime.datetime.now().strftime("%Y-%m-%d")
    Strtoday = datetime.datetime.now().strftime("%Y%m%d")
    Strorder= OrderCodes[:8]
    ordertime=Strorder[:4]+'-'+Strorder[4:6]+'-'+Strorder[-2:]
    if Strtoday==Strorder:
        check_currency = tabelname.query.filter_by(Category=CLSKUS,datetime = todaytime,\
            OrderSourceName=irobotboxs1.OrderSourceName,Currency=irobotboxs1.Currency).first()

        if check_currency:
            check_currency.TotalPrice=irobotboxs1.TotalPrice
            check_currency.number=ProductNums
            db.session.add(check_currency)
        else:
            totalset = tabelname(Category=CLSKUS,OrderSourceName=irobotboxs1.OrderSourceName\
                ,datetime = todaytime,TotalPrice = irobotboxs1.TotalPrice,\
                number=ProductNums,Currency=irobotboxs1.Currency)
            db.session.add(totalset)
    else:
        check_currency = tabelname.query.filter_by(Category=CLSKUS,datetime = ordertime,\
            OrderSourceName=irobotboxs1.OrderSourceName,Currency=irobotboxs1.Currency).first()
        if check_currency:
            check_currency.TotalPrice=irobotboxs1.TotalPrice
            check_currency.number=ProductNums
            db.session.add(check_currency)
        else:
            totalset = tabelname(Category=CLSKUS,OrderSourceName=irobotboxs1.OrderSourceName,\
                datetime = ordertime,TotalPrice = irobotboxs1.TotalPrice,\
                number=ProductNums,Currency=irobotboxs1.Currency)
            db.session.add(totalset)