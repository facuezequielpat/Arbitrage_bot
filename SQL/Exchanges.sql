--drop database if exists Exchanges;
--create database Exchanges;
--use Exchanges;
CREATE TABLE EXCHANGE (
	ID SERIAL PRIMARY KEY, --Serial = Auto increment OK
	NOMBRE VARCHAR(50) NOT NULL UNIQUE, -- Unique = No se puede repetir el dato OK
	ACTIVE BOOLEAN DEFAULT TRUE --OK
);

CREATE TABLE ADVERTISER_P2P (
	ID_TEXT TEXT PRIMARY KEY,
	--id_integer BIGINT GENERATED ALWAYS AS (id_text::BIGINT) STORED UNIQUE,     -- versión numérica (indexable)
	EXCHANGE_ID INT NOT NULL REFERENCES EXCHANGE (ID), -- Un anunciante pertenece a un exchange
	NICKNAME VARCHAR(100), --OK
	ORDERCOUNT INT, --OK Contar ordenes completadas
	--monthOrderCount INT,--NO poner nunca es igual a completedOrderNumOfLatest30day
	MONTHFINISHRATE NUMERIC(5, 2), -- porcentaje finalisado del mes -- OK
	POSITIVERATE NUMERIC(5, 2), -- porcentaje -- OK
	AVGRELEASETIMEOFLATEST_30DAY NUMERIC(10, 2), --OK Tiempo promedio de liberación últimos 30 días (s) PUEDE SER NULO
	AVGPAYTIMEOFLATEST_30DAY NUMERIC(10, 2), --OK Tiempo promedio de pago últimos 30 días (s) PUEDE SER NULO
	COMPLETEDORDERNUMOFLATEST30DAY NUMERIC(10, 2), -- OK Total órdenes completadas últimos 30 días
	KYC VARCHAR(100), --OK
	LASTACTIVETIME BIGINT -- OK
);*/

-- Anuncios P2P (ads)
CREATE TABLE ADS_P2P (
	ID_TEXT TEXT UNIQUE,
	DATE_TIME TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- OK
	EXCHANGE_ID INT NOT NULL REFERENCES EXCHANGE (ID), -- el anuncio pertenece a un exchange
	--ADVERTISER_ID TEXT REFERENCES ADVERTISER_P2P (ID_TEXT), -- el anuncio lo publica un anunciante
	ASSET VARCHAR(10) NOT NULL, -- USDT, BTC, etc -- OK
	FIAT VARCHAR(10) NOT NULL, -- ARS, USD, BRL, etc -- OK
	TYPE VARCHAR(10) NOT NULL, -- BUY o SELL --OK
	PRICE NUMERIC(18, 2), -- API STRING CAMBIAR A NUMERICO
	VOLUME NUMERIC(18, 6), -- API STRING CAMBIAR A NUMERICO tradableQuantity
	LIQUIDITY NUMERIC(18, 6), --OK
	MIN_AMOUNT NUMERIC(18, 2), -- API STRING CAMBIAR A NUMERICO minSingleTransAmount
	MAX_AMOUNT NUMERIC(18, 2), -- API STRING CAMBIAR A NUMERICO maxSingleTransAmount
	PAYTIMELIMIT INT, --OK
	REMARK TEXT, -- Terminos y condiciones del anuncio
	MY_AD BOOLEAN DEFAULT NULL,
	-- creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP --Current_TimeStamp = fecha y hora actual del servidor
	PRIMARY KEY (ID_TEXT, DATE_TIME)
);

CREATE TABLE PAYMENT_METHODS (
	ID SERIAL PRIMARY KEY,
	EXCHANGE_ID INT NOT NULL REFERENCES EXCHANGE(ID),
	PAY_TYPE VARCHAR(100), -- Ej: "MercadoPago", "Bank Transfer"
	TRADEMETHODNAME VARCHAR(200),
	FIAT VARCHAR(20)
);

CREATE TABLE ADS_PAYMENT_METHODS (
	ADS_ID TEXT NOT NULL REFERENCES ADS_P2P (ID_TEXT),
	PAYMENT_METHOD_ID INT NOT NULL REFERENCES PAYMENT_METHODS (ID),
	PRIMARY KEY (ADS_ID, PAYMENT_METHOD_ID) -- evita duplicados
);

CREATE TABLE ORDERS_P2P (
	ID_TEXT TEXT PRIMARY KEY, -- Identificador interno -- "orderNumber"
	--id_integer BIGINT GENERATED ALWAYS AS (id_text::BIGINT) STORED UNIQUE,
	ADS_ID TEXT NOT NULL REFERENCES ADS_P2P (ID_TEXT), -- "advNo"
	PAYMENT_METHOD_ID INT NOT NULL REFERENCES PAYMENT_METHODS (ID),
	TRADE_TYPE VARCHAR(10) NOT NULL, -- "SELL" / "BUY"
	CRYPTO VARCHAR(10) NOT NULL, -- Cripto (ej: BUSD, USDT)
	FIAT VARCHAR(10) NOT NULL, -- Moneda fiat (ej: CNY, ARS, USD)
	AMOUNT_CRYPTO NUMERIC(36, 8) NOT NULL, -- Cantidad en cripto
	TOTAL_PRICE_FIAT NUMERIC(36, 8) NOT NULL, -- Precio total en fiat
	UNIT_PRICE NUMERIC(36, 8) NOT NULL, -- Precio unitario en fiat
	ORDER_STATUS VARCHAR(30) NOT NULL, -- Estado de la orden
	CREATE_TIME BIGINT NOT NULL, -- Epoch timestamp en milisegundos
	COMMISSION_CRYPTO NUMERIC(36, 8) DEFAULT 0, -- Comisión (en cripto)
	COUNTER_PART_NICKNAME VARCHAR(100), -- Nickname de contraparte
	ADVERTISEMENT_ROLE VARCHAR(50) NOT NULL -- MAKER / TAKER
);

CREATE TABLE MESSAGES_P2P (
	ID_TEXT TEXT PRIMARY KEY, -- el original de la API
	--id_integer BIGINT GENERATED ALWAYS AS (id_text::BIGINT) STORED,     -- versión numérica (indexable)
	UUID UUID, -- UUID del mensaje (traído por la API)
	ORDERS_ID TEXT NOT NULL REFERENCES ORDERS_P2P (ID_TEXT),
	TYPE VARCHAR(20), -- Tipo de mensaje (system, text, etc.)
	SUB_TYPE VARCHAR(50), -- Subtipo del mensaje (si aplica)
	ORDER_NO TEXT, -- Número de orden (string en la API)
	CONTENT TEXT, -- Contenido (puede ser texto o JSON en string)
	IMAGE_URL TEXT, -- URL de imagen
	IMAGE_TYPE VARCHAR(50), -- Tipo de imagen
	STATUS VARCHAR(20), -- Estado del mensaje (read, unread)
	CREATE_TIME TIMESTAMPTZ, -- Fecha/hora del mensaje en tu zona horaria
	SELF VARCHAR(20), -- Si lo envió el propio usuario
	FILE_URL TEXT -- URL de archivo adjunto
	-------------source_lang_name VARCHAR(50),              -- Idioma original NO SIRVE
	-------------target_lang_name VARCHAR(50)               -- Idioma destino NO SIRVE
);

SELECT
	*
FROM
	ADS_P2P;

SELECT
	*
FROM
	PAYMENT_METHODS WHERE EXCHANGE_ID = 1;

ALTER TABLE PAYMENT_METHODS
ALTER COLUMN TRADEMETHODNAME TYPE VARCHAR(200);

ALTER TABLE PAYMENT_METHODS 
ADD CONSTRAINT UNIQUE_PAYMENT UNIQUE (EXCHANGE_ID, PAY_TYPE, FIAT);


