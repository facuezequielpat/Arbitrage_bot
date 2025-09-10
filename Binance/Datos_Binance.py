import requests
import json
import asyncio

class BinanceP2P():
    # 1️⃣ URL para buscar anuncios
    SEARCH_URL = "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"#OK
    DETAIL_ADS_URL  = "https://p2p.binance.com/bapi/c2c/v2/public/c2c/adv/detail?advNo="
    FILTER_CONDITIONS_URL = "https://p2p.binance.com/bapi/c2c/v2/public/c2c/adv/filter-conditions"# Metodos de pago OK
    DETAIL_ADVERTISER_URL= "https://c2c.binance.com/bapi/c2c/v2/friendly/c2c/user/profile-and-ads-list?userNo="
    GROUP_URL="https://c2c.binance.com/bapi/c2c/v2/private/c2c/chat/groups"# ME DA LOS DATOS DEL GRUPO INCLUIDO EL ID
    CHAT_URL = "https://c2c.binance.com/bapi/c2c/v2/private/c2c/chat/query-chat-by-page?rows=50&page=1&groupId="# CAMBIAR EL GRUPO ID POR EL CORRESPONDIENTE
    CHAT_URL2="&direction=up&entry=P2P"
    def __init__(self):
       self.headers = {"Content-Type": "application/json"} #Le dice a la API que los datos enviados y recibidos serán en formato JSON. 

    def get_payment_methods(self, fiat: str):
        payload = {"fiat": fiat}
        resp = requests.post(self.FILTER_CONDITIONS_URL, headers=self.headers, data=json.dumps(payload))
        data = resp.json()
        if "data" not in data or "tradeMethods" not in data["data"]:
            raise ValueError(f"No se pudo obtener métodos de pago para {fiat}")
        else:
            methods = {method["tradeMethodName"]: method["identifier"] for method in data["data"]["tradeMethods"]}
            tradeMethodName = [method["tradeMethodName"] for method in data["data"]["tradeMethods"]]
            identifiers = [method["identifier"] for method in data["data"]["tradeMethods"]]
            return [methods, tradeMethodName, identifiers]

    def search_ads(self, asset: str, fiat: str, rows: str, pay_types: list, trade_type: str, page=1) -> dict:
        payload = {
            "asset": asset,
            "fiat": fiat,
            "tradeType": trade_type,
            "page": page,
            "rows": rows,
            "payTypes": pay_types
        }
        resp = requests.post(self.SEARCH_URL, headers=self.headers, data=json.dumps(payload))
        data = resp.json()
        return data

    def get_ad_details(self, adv_id: str) -> dict:
        resp = requests.get(self.DETAIL_ADS_URL + adv_id, headers=self.headers)
        data = resp.json()
        data = data["data"]["remarks"]
        return data
    
    def get_advertiser_details(self, user_no: str) -> dict:
        resp = requests.get(self.DETAIL_ADVERTISER_URL + user_no, headers=self.headers)
        data = resp.json()
        data_user = data["data"]["userDetailVo"]
        data_user_stats= data_user["userStatsRet"]
        data_user_KYC= data_user["userKycRet"]
        return [data_user, data_user_stats, data_user_KYC]

    def get_chat_group(self):
        Payload = {
            "contactType": 0,
            "entry": "P2P",
            "page": 1,
            "rows": 10
        }
        resp = requests.get(self.GROUP_URL , headers=self.headers, params=Payload)
        data = resp.json()
        data_grupoId = data ["data"]["groupId"]
        return data_grupoId
    
    def get_chat_messages(self, group_id: str):
        PAYLOAD = {
            "rows": 50,
            "page": 1,
            "groupId": group_id,
            "direction": "up",
            "entry": "P2P"
        }
        resp = requests.get(self.CHAT_URL + "?groupId=" + group_id + self.CHAT_URL2, headers=self.headers, params=PAYLOAD)
        data = resp.json()
        data = data["data"]
        return data

