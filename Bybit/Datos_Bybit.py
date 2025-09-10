from bybit_p2p import P2P
import json
import os
from dotenv import load_dotenv
import requests


load_dotenv("C:\\Users\\Usuario\\Desktop\\Facu\\TPs de Facu\\Bot de Arbitraje\\Keys.env")
class BybitP2P():
    
    def __init__(self):
        self.API_KEY = os.getenv("apiKeybit")
        self.API_SECRET = os.getenv("secretKeybit")
        self.client = P2P(testnet=False, api_key=self.API_KEY, api_secret=self.API_SECRET)
        
    def ads (self,tokenId:str,currencyId:str,side:str,size:str="500"):
        '''Obtiene anuncios P2P en Bybit.'''
        anuncios_online = self.client.get_online_ads(
            tokenId=tokenId,
            currencyId=currencyId,
            side=side,
            size=size)["result"]["items"]

        return anuncios_online
    
    def my_ads(self):
        '''Obtiene mis anuncios P2P en Bybit.'''
        my_ads = self.client.get_my_ads()["result"]["items"]
        return my_ads

    def orders_finished(self):
        '''Obtiene las ordenes finalizadas en Bybit.'''
        orders_finished = self.client.get_orders(
            page=1,
            size=50,
            status=50
        )["result"]["items"]
        return orders_finished
    def orders_pendings(self):
        orders_pendings = self.client.get_pending_orders(
            page=1,
            size=50
        )["result"]["items"]
        return orders_pendings
    def order_details(self, orderId:str):
        '''Obtiene los detalles de una orden en Bybit.'''
        order_details = self.client.get_order_details(orderId=orderId)["result"]
        return order_details

    def chat_messages(self, orderId:str):
        chat_messages = self.client.get_chat_messages(
            orderId=orderId,
            size="100"
            )["result"]["items"]
        return chat_messages

    def advertiser(self, anuncios, orders_finished):
        #descripcion_anuncios_sell, descripcion_anuncios_buy = self.descripcion_anuncios()
        advertiser_ids= [anuncio["userId"] for anuncio in anuncios]
        orders_ids = [order["orderId"] for order in orders_finished]
        #advertiser_ids_buy = [anuncio["userId"] for anuncio in anuncios]
        detalles_advertisers = [self.client.get_counterparty_info(originalUid=str(uid), orderId=str(oid)) for uid, oid in zip(advertiser_ids, orders_ids)]
        #detalles_advertisers_buy = [self.client.get_counterparty_info(originalUid=str(uid)) for uid in advertiser_ids_buy]
        return detalles_advertisers
    
    def traduct_payments(self):
        
            URL_PAYMENTS="https://paste.nk.ax/api/raw/7u2UfJbbS6YYRvx"

            response = requests.get(URL_PAYMENTS)

            text = response.content.decode("utf-8-sig")

            #bs4= BeautifulSoup(response.text, "html.parser")
            json_data = json.loads(text)


            paymentConfigVo = json_data['result']["paymentConfigVo"]

            currencyPaymentIdMap = json_data["result"]["currencyPaymentIdMap"]

            #json_data = {item['paymentType']: item['paymentName'] for item in json_data['result']["paymentConfigVo"]}
            #print(type(json_data))
            #json_data=json.dumps(json_data, indent=4, ensure_ascii=False)

            return paymentConfigVo, currencyPaymentIdMap

#print(BybitP2P().advertiser())
#print(BybitP2P().descripcion_anuncios())
#BybitP2P().traduct_payments()


"""lista_payments_NameId={"Bank Transfer":"14","Bank Transfer (Argentina)":"196", 
                        "Facebank International":"206","Pipol Pay":"116",
                        "PayPal":"54","Skrill":"162","NETELLER":"111",
                        "Zinli":"189","Wise":"78",
                        "AirTM":"7","N26":"156",
                        "Payeer":"51","Volet.com (Formerly Advcash)":"5",
                        "Google Pay":"29","AlipayHK":"2","Perfect Money":"56",
                        "Uala":"134","MercadoPago":"129",
                        "Lemon Cash":"128","Banco del sol":"124",
                        "Prex":"131", "Banco Brubank":"123"}

    lista_payments_IdName = {
        "14": "Bank Transfer",
        "196": "Bank Transfer (Argentina)",
        "206": "Facebank International",
        "116": "Pipol Pay",
        "54": "PayPal",
        "162": "Skrill",
        "111": "NETELLER",
        "189": "Zinli",
        "78": "Wise",
        "7": "AirTM",
        "156": "N26",
        "51": "Payeer",
        "5": "Volet.com (Formerly Advcash)",
        "29": "Google Pay",
        "2": "AlipayHK",
        "56": "Perfect Money",
        "131": "Prex",
        "123": "Banco Brubank",
        "167": "Uphold"
    }


    lista_crypto=[
        "USDT"
    ]

    lista_fiat=[
        "USD", 
        "EUR",  
        "ARS"
    ]
    return traducciones, lista_payments_IdName, lista_crypto, lista_fiat    

for i, anuncio in enumerate(descripcion_anuncios_sell, 1):
    # Verificar si hay algún payment del anuncio que esté en nuestra lista de IDs
    if any(payment_id in lista_payments_IdName for payment_id in anuncio.get("payments", [])):
        print("=" * 60)
        print(f"Anuncio {i}:")
        for clave, valor in anuncio.items():
            clave_es = traducciones.get(clave, clave)
            if clave == "payments":
                # Convertir IDs a nombres de métodos de pago
                nombres_payments = [lista_payments_IdName.get(pid, pid) for pid in valor]
                print(f"  {clave_es}: {', '.join(nombres_payments)}")
            else:
                print(f"  {clave_es}: {valor}")"""

#print(anuncio_filtrado)
