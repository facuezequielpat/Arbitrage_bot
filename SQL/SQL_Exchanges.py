import psycopg2
import json
import asyncio
from datetime import datetime, timedelta
from Binance.Procesar_Data_Binance import ProcesarDataBinance
from Bybit.Procesar_Data_Bybit import ProcesarDataBybit

client = ProcesarDataBinance()
client2 = ProcesarDataBybit()
class DatabaseManager:
    def __init__(self,client,client2):
        self.client = client
        self.client2 = client2
        self.conn = None

    def connect(self):
        """Establece la conexión a la base de datos."""
        try:
            self.conn = psycopg2.connect(
                host="LOCALHOST",
                port=5432,
                database="Exchanges",
                user="postgres",
                password="L_12345upin"
            )
            print("Conexión a la base de datos establecida.")
        except psycopg2.OperationalError as e:
            print(f"Error al conectar a la base de datos: {e}")
            self.conn = None

    def close(self):
        """Cierra la conexión a la base de datos."""
        if self.conn:
            self.conn.close()
            print("Conexión a la base de datos cerrada.")

    def insert_ads(self):
        """Inserta o actualiza los datos de los anuncios en la tabla 'ads'."""
        if not self.conn:
            self.connect()

        cursor = self.conn.cursor()
        insert_query = """
                INSERT INTO ads_p2p (id_text, exchange_id, asset, fiat, type, price, volume, liquidity, min_amount, max_amount, payTimeLimit, remark)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (ID_TEXT , DATE_TIME) DO NOTHING;
        """
        procesar_anuncios=list(self.client.procesar_anuncios_y_metodos_de_pago(self.client.procesar_anuncios()))
        for ads, payments in procesar_anuncios:
            cursor.execute(insert_query, tuple(ads[:12]))
            print(len(ads), ads)
            '''for id_text, exchange_id, asset, fiat, type, price, volume, liquidity, min_amount, max_amount, payTimeLimit, remark  in ads:
                cursor.execute(insert_query, (id_text,  exchange_id, asset, fiat, type, price, volume, liquidity, min_amount, max_amount, payTimeLimit, remark))'''

        procesar_anuncios_2=list(self.client2.process_ads_and_ads_payments_methods())
        for ads, payments in procesar_anuncios_2:
            cursor.execute(insert_query, tuple(ads[:12]))
            print(len(ads), ads)
            '''for id_text, exchange_id, asset, fiat, type, price, volume, liquidity, min_amount, max_amount, payTimeLimit, remark in ads:
                cursor.execute(insert_query, (id_text, exchange_id, asset, fiat, type, price, volume, liquidity, min_amount, max_amount, payTimeLimit, remark))'''
        self.conn.commit()
        cursor.close()

    def insert_ads_payments_methods(self):
        """Inserta o actualiza los datos de los anuncios en la tabla 'ads'."""
        if not self.conn:
            self.connect()

        cursor = self.conn.cursor()
        insert_query = """
                INSERT INTO ADS_PAYMENT_METHODS (ADS_ID, PAYMENT_METHOD_ID)
                SELECT a.ID_TEXT, pm.ID
                FROM ADS_P2P a
                JOIN PAYMENT_METHODS pm 
                ON pm.EXCHANGE_ID = a.EXCHANGE_ID
                AND pm.FIAT = a.FIAT
                WHERE a.ID_TEXT = %s
                AND pm.PAY_TYPE = %s
                ON CONFLICT (ADS_ID, PAYMENT_METHOD_ID) DO NOTHING;
                """
        # Procesar anuncios de Binance
        procesar_anuncios=list(self.client.procesar_anuncios_y_metodos_de_pago(self.client.procesar_anuncios()))
        for ads, payments in procesar_anuncios:
            cursor.execute(insert_query, tuple(payments[:2]))

        # Procesar anuncios de Bybit
        procesar_anuncios_2=list(self.client2.process_ads_and_ads_payments_methods())
        for ads, payments in procesar_anuncios_2:
            cursor.execute(insert_query, tuple(payments[:2]))
        self.conn.commit()
        cursor.close()


    def insert_payments_methods(self):
        """Inserta o actualiza los métodos de pago en la tabla 'payment_methods'."""
        if not self.conn:
            self.connect()

        print(list(self.client.procesar_payments_methods()))
        print(list(self.client2.process_traduct_payments()))
        cursor = self.conn.cursor()
        insert_query = """
                INSERT INTO payment_methods (exchange_id, pay_type, tradeMethodName, fiat)
               VALUES (%s, %s, %s, %s);
                """
        # Procesar métodos de Binance

        for exchange_id, pay_type, tradeMethodName, fiat in self.client.procesar_payments_methods():

                cursor.execute(insert_query,(exchange_id,pay_type,tradeMethodName,fiat))

        # Procesar métodos de Bybit
        for exchange_id, pay_type, tradeMethodName, fiat in self.client2.process_traduct_payments():
                cursor.execute(insert_query,(exchange_id,pay_type,tradeMethodName,fiat))
        self.conn.commit()
        cursor.close()
        self.conn.close()

    
database_manager = DatabaseManager(client=client, client2=client2)
#database_manager.insert_payments_methods()
#database_manager.insert_ads()
database_manager.insert_ads_payments_methods()
'''def insert_advertiser_ads_Binance(self):
        """Inserta o actualiza los datos de los anunciantes en la tabla 'advertisers' con el exchange de Binance."""
        if not self.conn:
            self.connect()

        cursor = self.conn.cursor()
        insert_query = """
                INSERT INTO ADVERTISER_P2P (
    ID_TEXT,
    EXCHANGE_ID,
    NICKNAME,
    ORDERCOUNT,
    MONTHFINISHRATE,
    POSITIVERATE,
    AVGRELEASETIMEOFLATEST30DAY,
    AVGRELEASETIMEOFLATEST,
    AVGPAYTIMEOFLATEST30DAY,
    AVGPAYTIMEOFLATEST,
    COMPLETEDORDERNUMOFLATEST30DAY,
    KYC,
    LASTACTIVETIME
)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
ON CONFLICT (ID_TEXT) DO UPDATE SET
    NICKNAME = EXCLUDED.NICKNAME,
    ORDERCOUNT = EXCLUDED.ORDERCOUNT,
    MONTHFINISHRATE = EXCLUDED.MONTHFINISHRATE,
    POSITIVERATE = EXCLUDED.POSITIVERATE,
    AVGRELEASETIMEOFLATEST30DAY = EXCLUDED.AVGRELEASETIMEOFLATEST30DAY,
    AVGRELEASETIMEOFLATEST = EXCLUDED.AVGRELEASETIMEOFLATEST,
    AVGPAYTIMEOFLATEST30DAY = EXCLUDED.AVGPAYTIMEOFLATEST30DAY,
    AVGPAYTIMEOFLATEST = EXCLUDED.AVGPAYTIMEOFLATEST,
    COMPLETEDORDERNUMOFLATEST30DAY = EXCLUDED.COMPLETEDORDERNUMOFLATEST30DAY,
    KYC = EXCLUDED.KYC,
    LASTACTIVETIME = EXCLUDED.LASTACTIVETIME;
        """
        for id_text, exchange_id, nickName, orderCount, monthFinishRate, positiveRate, avgReleaseTimeOfLatest30day, avgReleaseTimeOfLatest, avgPayTimeOfLatest30day, avgPayTimeOfLatest, completedOrderNumOfLatest30day, KYC, lastActiveTime in self.client.procesar_advertisers_sell_and_buy():
            cursor.execute(insert_query, (id_text, exchange_id, nickName, orderCount, monthFinishRate, positiveRate, avgReleaseTimeOfLatest30day, avgReleaseTimeOfLatest, avgPayTimeOfLatest30day, avgPayTimeOfLatest, completedOrderNumOfLatest30day, KYC, lastActiveTime))

        for id_text, exchange_id, nickName, orderCount, monthFinishRate, positiveRate, avgReleaseTimeOfLatest30day, avgReleaseTimeOfLatest, avgPayTimeOfLatest30day, avgPayTimeOfLatest, completedOrderNumOfLatest30day, KYC, lastActiveTime in self.client2.process_advertiser_ads():
            cursor.execute(insert_query, (id_text, exchange_id, nickName, orderCount, monthFinishRate, positiveRate, avgReleaseTimeOfLatest30day, avgReleaseTimeOfLatest, avgPayTimeOfLatest30day, avgPayTimeOfLatest, completedOrderNumOfLatest30day, KYC, lastActiveTime))
        
        self.conn.commit()
        cursor.close()

    def insert_advertiser_orders_Bybit(self):
        """Inserta o actualiza los datos de los anunciantes en la tabla 'advertisers' con el exchange de Bybit."""
        if not self.conn:
            self.connect()

        cursor = self.conn.cursor()
        insert_query = """
                INSERT INTO ADVERTISER_P2P (
    ID_TEXT,
    EXCHANGE_ID,
    NICKNAME,
    ORDERCOUNT,
    MONTHFINISHRATE,
    POSITIVERATE,
    AVGRELEASETIMEOFLATEST30DAY,
    AVGRELEASETIMEOFLATEST,
    AVGPAYTIMEOFLATEST30DAY,
    AVGPAYTIMEOFLATEST,
    COMPLETEDORDERNUMOFLATEST30DAY,
    KYC,
    LASTACTIVETIME
)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
ON CONFLICT (ID_TEXT) DO UPDATE SET
    NICKNAME = EXCLUDED.NICKNAME,
    ORDERCOUNT = EXCLUDED.ORDERCOUNT,
    MONTHFINISHRATE = EXCLUDED.MONTHFINISHRATE,
    POSITIVERATE = EXCLUDED.POSITIVERATE,
    AVGRELEASETIMEOFLATEST30DAY = EXCLUDED.AVGRELEASETIMEOFLATEST30DAY,
    AVGRELEASETIMEOFLATEST = EXCLUDED.AVGRELEASETIMEOFLATEST,
    AVGPAYTIMEOFLATEST30DAY = EXCLUDED.AVGPAYTIMEOFLATEST30DAY,
    AVGPAYTIMEOFLATEST = EXCLUDED.AVGPAYTIMEOFLATEST,
    COMPLETEDORDERNUMOFLATEST30DAY = EXCLUDED.COMPLETEDORDERNUMOFLATEST30DAY,
    KYC = EXCLUDED.KYC,
    LASTACTIVETIME = EXCLUDED.LASTACTIVETIME;
        """
        for id_text, exchange_id, nickName, orderCount, monthFinishRate, positiveRate, avgReleaseTimeOfLatest30day, avgReleaseTimeOfLatest, avgPayTimeOfLatest30day, avgPayTimeOfLatest, completedOrderNumOfLatest30day, KYC, lastActiveTime in self.client2.process_advertiser_orders():
            cursor.execute(insert_query, (id_text, exchange_id, nickName, orderCount, monthFinishRate, positiveRate, avgReleaseTimeOfLatest30day, avgReleaseTimeOfLatest, avgPayTimeOfLatest30day, avgPayTimeOfLatest, completedOrderNumOfLatest30day, KYC, lastActiveTime))'''