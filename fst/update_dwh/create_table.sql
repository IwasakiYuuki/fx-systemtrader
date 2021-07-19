create table if not exists `fx-systemtrader-dev.fx_features.usd_jpy_s5_candle` (
	id INTEGER NOT NULL,
	candleFormat STRING,
	openMid FLOAT64,
	highMid FLOAT64,
	lowMid FLOAT64,
	closeMid FLOAT64,
	openBid FLOAT64,
	openAsk FLOAT64,
	highBid FLOAT64,
	highAsk FLOAT64,
	lowBid FLOAT64,
	lowAsk FLOAT64,
	closeBid FLOAT64,
	closeAsk FLOAT64,
	volume INTEGER NOT NULL,
	time TIMESTAMP NOT NULL,
)
options(
	description="a table that USD_JPY s5 candles"
)
