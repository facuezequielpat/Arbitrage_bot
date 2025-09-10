from Binance.Datos_Binance import BinanceP2P
import asyncio

cliente = BinanceP2P()
class ProcesarDataBinance():

    def __init__(self):
        self.cliente = cliente
        self.data_list = []
        self.lista_payments={
        "lista_payments_USD"  : [
            #"Bank Transfer",
            #"Bank Transfer (Argentina)",
            "Facebank International",
            "Pipol Pay",
            "Skrill (Moneybookers)",
            "Neteller",
            "Zinli",
            "AirTM",
            "N26",
            "Payeer",
            #"Google Pay (GPay)",
            #"Perfect Money",
            "Mercadopago",
            "Prex",
            "Banco Brubank",
            #"Uphold",
            "Global66",
            "GrabrFi"
        ]
        #,
        #"lista_payments_EUR":[
            #"Bank Transfer",
            #"SEPA (EU) bank transfer",
            #"N26",
            #"Payeer"
            #"Perfect Money"
        #]
        
        #'''"lista_payments_ARS":[
        #    "Bank Transfer (Argentina)",
        #    "Bank Transfer",
        #    "Mercadopago",
        #    "Uala",
        #    "Lemon Cash",
        #    "Banco del Sol",
        #    "Prex",
        #   "Banco Brubank"
        #]   
        }

        # data{ countrys,  tradeMethods [{identifier:"Zelle", tradeMethodName:"Zelle"}{}{}]}
        #hacer diccionario de listas de metodos de pago por cada fiat.
        #lista_payments=[lista_payments_USD, lista_payments_EUR, lista_payments_ARS]

        self.lista_crypto=[
            "USDT"
        ]

        self.lista_fiat=[
            "USD"
            #"EUR", 
            #"ARS",
            #"BRL",
            #"MXN",
            #"PEN",
            #"UYU",
            #"GBP",
            #"NZD",
            #"AUD",
            #"CAD"

        ]

        
        self.type = ["BUY", "SELL"]

    
    def procesar_anuncios(self):

        for fiat, payments in zip(self.lista_fiat, self.lista_payments.values()):
            try:
                methods = self.cliente.get_payment_methods(fiat)[0]
            except ValueError as e:
                print(e)
                continue

            for payment_name in payments:
                if payment_name not in methods:
                    print(f"⚠️ '{payment_name}' no disponible para {fiat}")
                    continue

                for crypto in self.lista_crypto:

                    for trade_type in self.type:

                    #asset: str, fiat: str, trade_type: str, rows: int, pay_types: list
                        data_list = self.cliente.search_ads(crypto, fiat, 20 , [methods[payment_name]], trade_type)
                        

                        if payment_name not in methods:
                            print(f"⚠️ '{payment_name}' no disponible para {fiat}")
                            continue

                        if not data_list.get("success"):
                            print(data_list)
                            print(f"⚠️ Error: {data_list.get('message')}")
                            continue
                        if not data_list.get("data"):
                            print("⚠️ No se recibieron anuncios para los parámetros dados: Sell ")
                            continue

                        self.data_list.append(data_list)
                        yield data_list


    def procesar_anuncios_y_metodos_de_pago(self, data_list):

        for data in data_list:
            for adv_info in data["data"]:
            
                adv = adv_info["adv"]
                for i in adv["tradeMethods"]:
                    pay_type = str(i["payType"])
                    id_text = str(adv["advNo"])# ID único del anuncio
                    exchange_id=1
                    #advertiser_id=str(adv_info["advertiser"]["userNo"])#ID advertiser
                    asset = str(adv["asset"])
                    fiat = str(adv["fiatUnit"])
                    type = str(adv["tradeType"])
                    price = float(adv["price"])
                    volume = float(adv["tradableQuantity"])
                    liquidity = float(price * volume)
                    min_amount = float(adv["minSingleTransAmount"])
                    max_amount = float(adv["maxSingleTransAmount"])
                    payTimeLimit = int(adv["payTimeLimit"])
                    remark = str(self.cliente.get_ad_details(id_text))
                    
                    yield [id_text, exchange_id, asset, fiat, type, price, volume, liquidity, min_amount, max_amount, payTimeLimit, remark],[id_text, pay_type]

    def procesar_advertiser_sell_and_buy(self,data_list):

        for data in data_list:
            for adv_info in data["data"]:

                advertiser = self.cliente.get_advertiser_details(adv_info["advertiser"]["userNo"])
                advertiser2 = adv_info["advertiser"]

                id_text= str(advertiser[0]["userNo"])
                exchange_id = 1
                #realName=str(advertiser[0]["realName"])
                nickName=str(advertiser[0]["nickName"])
                orderCount=int(advertiser[0]["orderCount"])
                #monthOrderCount=int(advertiser[0]["monthOrderCount"])
                monthFinishRate=float(advertiser[0]["monthFinishRate"])
                positiveRate=float(advertiser2["positiveRate"])
                #advConfirmTime_sell=advertiser_sell[0]["advConfirmTime"]
                avgReleaseTimeOfLatest30day=float(advertiser[1]["avgReleaseTimeOfLatest30day"])
                avgReleaseTimeOfLatest=None
                avgPayTimeOfLatest30day=float(advertiser[1]["avgPayTimeOfLatest30day"])
                avgPayTimeOfLatest=None
                completedOrderNumOfLatest30day=float(advertiser[1]["completedOrderNumOfLatest30day"])
                KYC=str(advertiser[2]["addressStatus"])
                lastActiveTime=int(advertiser[0]["lastActiveTime"] or 0)

                yield id_text, exchange_id, nickName, orderCount, monthFinishRate, positiveRate, avgReleaseTimeOfLatest30day, avgReleaseTimeOfLatest, avgPayTimeOfLatest30day, avgPayTimeOfLatest, completedOrderNumOfLatest30day, KYC, lastActiveTime

            """advertiser_buy=self.cliente.get_advertiser_details(adv_info_buy["advertiser"]["userNo"])
            advertiser_buy2 = adv_info_buy["advertiser"]#

            id_buy = str(advertiser_buy[0]["userNo"])
            realName_buy=str(advertiser_buy[0]["realName"])
            nickName_buy=str(advertiser_buy[0]["nickName"])
            orderCount_buy=int(advertiser_buy[0]["orderCount"])
            monthOrderCount_buy=int(advertiser_buy[0]["monthOrderCount"])
            monthFinishRate_buy=float(advertiser_buy[0]["monthFinishRate"])
            positiveRate_buy=float(advertiser_buy2["positiveRate"])
            #advConfirmTime_buy=advertiser_buy[0]["advConfirmTime"]
            avgReleaseTimeOfLatest30day_buy=float(advertiser_buy[1]["avgReleaseTimeOfLatest30day"])
            avgReleaseTimeOfLatest_buy=None
            avgPayTimeOfLatest30day_buy=float(advertiser_buy[1]["avgPayTimeOfLatest30day"])
            avgPayTimeOfLatest_buy=None
            completedOrderNumOfLatest30day_buy=float(advertiser_buy[1]["completedOrderNumOfLatest30day"])
            KYC_buy=str(advertiser_buy[2]["addressStatus"])
            activeTimeInSecond_buy=int(advertiser_buy[0]["activeTimeInSecond"])"""

            """yield id_buy, realName_buy, nickName_buy, orderCount_buy, monthOrderCount_buy, monthFinishRate_buy, positiveRate_buy, avgReleaseTimeOfLatest30day_buy, avgReleaseTimeOfLatest_buy, avgPayTimeOfLatest30day_buy, avgPayTimeOfLatest_buy, completedOrderNumOfLatest30day_buy, KYC_buy, activeTimeInSecond_buy"""


    def procesar_chat_messages(self):#Fijarse despues del mvp 1
        get_chat_group = self.cliente.get_chat_group()
        chat_messages = self.cliente.get_chat_messages(get_chat_group)
        id = chat_messages["id"]
        uuid = chat_messages["uuid"]
        type = chat_messages["type"]
        subType = chat_messages["subType"]
        orderNo = chat_messages["orderNo"]
        content = chat_messages["content"]
        imageUrl = chat_messages["imageUrl"]
        imageType = chat_messages["imageType"]
        status = chat_messages["status"]
        createTime = chat_messages["createTime"]
        self1 = chat_messages["self"]
        fileUrl = chat_messages["fileUrl"]
        sourceLangName = chat_messages["sourceLangName"]
        targetLangName = chat_messages["targetLangName"]

        yield id, uuid, type, subType, orderNo, content, imageUrl, imageType, status, createTime, self1, fileUrl, sourceLangName, targetLangName

    def procesar_payments_methods(self):
        for fiat in self.lista_fiat:
            try:
                methods, tradeMethodNames, identifiers = list(self.cliente.get_payment_methods(fiat))
                for Type, Name in zip(identifiers, tradeMethodNames):
                    exchange_id = 1
                    yield exchange_id, Type, Name, fiat
            except ValueError as e:
                print(e)


procesar_datos= ProcesarDataBinance()
anuncios= procesar_datos.procesar_anuncios()
anuncios_sell_and_buy= procesar_datos.procesar_anuncios_y_metodos_de_pago(anuncios)
#print(enumerate(anuncios_sell_and_buy))
#anunciantes_buy_and_sell= list(procesar_datos.procesar_advertiser_sell_and_buy(anuncios))
#print(enumerate(anunciantes_buy_and_sell))
#payments_methods= list(procesar_datos.procesar_payments_methods())
#print(payments_methods)