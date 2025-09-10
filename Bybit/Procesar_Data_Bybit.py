from Bybit.Datos_Bybit import BybitP2P
import json

cliente = BybitP2P()
class ProcesarDataBybit:
    def __init__(self):
        self.cliente = cliente
        self.list_fiat = ["USD"]
        self.list_cryptos = ["USDT"]
        self.list_side = ["1","0"]
        self.list_details_ads = ["id", "nickName", "userId", "currencyId", "tokenId", "price", "minAmount", "maxAmount", "payments", "remark", "paymentPeriod"]
        self.list_payments_Id = [
    "14", "196", "206", "116", "54", "162", "111", "189", "78", "7", "156",
    "51", "5", "29", "2", "56", "131", "123", "167"
                            ]
        self.list_details_orders = ["id", "side", "tokenId", "currencyId","notifyTokenQuantity", "amount", "price", "status", "status", "createDate", "fee"]
        self.list_details_orders2 = ["targetUserDisplays","targetNickName"]
        self.list_details_messages = ["id", "msgUuid", "msgType", "contentType", "orderId", "message", None, None, "isRead", "createDate", "roleType", None]

    def process_ads_and_ads_payments_methods(self):
        '''Procesa los anuncios y extrae la información relevante. 20 anuncios por combinacion de fiat, crypto, side y metodo de pago'''
        for fiat in self.list_fiat:
            for crypto in self.list_cryptos:
                for side in self.list_side:
                    ads= self.cliente.ads(crypto, fiat, side)
                    for payment_id in self.list_payments_Id:
                        count=0
                        for ad in ads:
                            if payment_id in ad["payments"]:
                                if count >= 20:
                                    break
                                id_text = str(ad["id"])
                                exchange_id = 2
                                #advertiser_id = int(ad["userId"])
                                asset = str(ad["tokenId"])
                                fiat = str(ad["currencyId"])
                                type = str(ad["side"])
                                price = float(ad["price"])
                                volume = float(ad["lastQuantity"])
                                liquidity = float(price * volume)
                                min_amount = float(ad["minAmount"])
                                max_amount = float(ad["maxAmount"])
                                payTimeLimit = int(ad["paymentPeriod"])
                                remark = str(ad["remark"])
                                pay_type = str(ad["payments"])
                                yield [id_text, exchange_id, asset, fiat, type, price, volume, liquidity, min_amount, max_amount, payTimeLimit, remark],[id_text, pay_type]

                                count += 1
                                

    def process_orders_finished(self): # Fijarse
        '''Procesa las ordenes finalizadas y extrae la información relevante.'''
        orders=self.cliente.orders_finished()
        for details in self.list_details_orders:
            for order in orders:
                yield order[details]
                for details2 in self.list_details_orders2:
                    order_details = self.cliente.order_details(orderId=order["id"])
                    yield order_details[details2]
    
    def process_pending_orders(self): # Fijarse
        '''Procesa las ordenes pendientes y extrae la información relevante.'''
        orders=self.cliente.orders_pendings()
        for details in self.list_details_orders:
            for order in orders:
                yield order[details]
                for details2 in self.list_details_orders2:
                    order_details = self.cliente.order_details(orderId=order["id"])
                    yield order_details[details2]

    def process_advertiser_orders(self):
        '''Procesa los anunciantes de las ordenes y extrae la información relevante.'''
        orders=self.cliente.orders_finished()
        for order in orders:
            advertiser=self.cliente.advertiser(originalUid=str(order["userId"]), orderId=str(order["id"]))
            id_text= str(advertiser["userId"])
            exchange_id=2
            #realName=str(advertiser["realName"])
            nickName=str(advertiser["nickName"])
            orderCount=int(advertiser["totalFinishCount"])
            monthFinishRate=float(advertiser["recentRate"])
            positiveRate=float(advertiser["goodAppraiseRate"])
            avgReleaseTimeOfLatest30day=None
            avgReleaseTimeOfLatest= float(advertiser["averageReleaseTime"])
            avgPayTimeOfLatest30day=None
            avgPayTimeOfLatest= float(advertiser["averageTransferTime"])
            completedOrderNumOfLatest30day=None
            KYC=str(advertiser["kycLevel"])
            lastActiveTime=int(advertiser["lastLogoutTime"])

            yield id_text, exchange_id, nickName, orderCount, monthFinishRate, positiveRate, avgReleaseTimeOfLatest30day, avgReleaseTimeOfLatest, avgPayTimeOfLatest30day, avgPayTimeOfLatest, completedOrderNumOfLatest30day, KYC, lastActiveTime

    # No sirve esta funcion para mi programa
    """def process_advertiser_ads(self):
        '''Procesa los anunciantes de los anuncios y extrae la información relevante.'''
        for fiat in self.list_fiat:
            for crypto in self.list_cryptos:
                for side in self.list_side:
                    ads= self.cliente.ads(crypto, fiat, side)
                    for ad in ads:
                        id_text = ad["userId"]
                        exchange_id = 2
                        nickName = ad["nickName"]
                        
                        yield str(id_text), exchange_id, str(nickName), None, None, None, None, None, None, None, None, None, None, None"""

    def process_pending_messages(self):
        orders=self.cliente.orders_pendings()
        for order in orders:
            messages = self.cliente.chat_messages(orderId=str(order["id"]))
            for message in messages:
                for detail in self.list_details_messages:
                    yield message[detail]

    def process_finished_messages(self):
        orders=self.cliente.orders_finished()
        for order in orders:
            messages = self.cliente.chat_messages(orderId=str(order["id"]))
            for message in messages:
                for detail in self.list_details_messages:
                    yield message[detail]

    def process_traduct_payments(self):#Se puede mejorar poniendo el fiat en una lista por metodo de pago
        paymentConfigVo, currencyPaymentIdMap = self.cliente.traduct_payments()
        for fiat, paymentType in json.loads(currencyPaymentIdMap).items():
            for payment in paymentConfigVo:
                for paymentId in paymentType:
                    if str(payment['paymentType']) == str(paymentId):
                        yield payment['paymentType'], payment['paymentName'], fiat
    
    

#resultados = list(enumerate(ProcesarDataBybit().process_ads()))
#print(resultados)