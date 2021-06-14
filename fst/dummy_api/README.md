# OANDA APIのダミー（開発環境用）
## 概要
OANDA APIの「レート取得」の関する処理を模倣したAPI．出力されるデータはすべて生成したダミーになっているがフォーマットなどは元のAPIと同様にしている．エラーの出力も同じフォーマットになっている．

## 背景
前提としてOANDA APIにはSandBox・開発・本番環境があり，SandBox環境だけはアクセストークン無しにAPIを使用できる．また，開発環境と本番環境の違いは使用する口座で，開発環境ではデモ口座を使用する．  
本システム（システムトレード）では本番（mainブランチ）と開発（developブランチ）に環境を分ける予定で，開発環境ではOANDA APIのSandBox環境，本番環境ではAPIの本番環境を使おうと思っていた．しかし実際にSandBox環境のAPIにリクエストを送ったが全く反応がなかったため使用不可と判断．（ドキュメントには「時々使用不可になる」と書いてあるが，むしろ「時々使用可能になる」ぐらいの頻度だと思う）  
そこで，GCP上のローカル環境でのみ接続できるダミーのAPIを自分で建てることにした．

## 現段階で実装している機能
- レート
  - 銘柄取得
  - 現在のレート取得
  - 過去のレート一括取得

## 実装予定の機能
- 注文
  - 取得
  - 作成
  - 情報取得
  - 内容変更
  - キャンセル

## 各機能の実行例（OANDAのドキュメントより）
### 銘柄取得
##### リクエスト
```bash
curl -X GET "http://api-sandbox.oanda.com/v1/instruments?accountId=12345&instruments=AUD_CAD%2CAUD_CHF"
```
##### レスポンス
```
{
  "instruments" : [
    {
      "instrument" : "AUD_CAD",
      "displayName" : "AUD\/CAD",
      "pip" : "0.0001",
      "maxTradeUnits" : 10000000
    },
    {
      "instrument" : "AUD_CHF",
      "displayName" : "AUD\/CHF",
      "pip" : "0.0001",
      "maxTradeUnits" : 10000000
    }
  ]
}
```

### 現在のレート取得
##### リクエスト
```bash
curl -X GET "http://api-sandbox.oanda.com/v1/prices?instruments=EUR_USD%2CUSD_JPY%2CEUR_CAD"
```
##### レスポンス
```
{
  "prices": [
    {
      "instrument":"EUR_USD",
      "time":"2013-06-21T17:41:04.648747Z",  // time in RFC3339 format
      "bid":1.31513,
      "ask":1.31528
    },
    {
      "instrument":"USD_JPY",
      "time":"2013-06-21T17:49:02.475381Z",
      "bid":97.618,
      "ask":97.633
    },
    {
      "instrument":"EUR_CAD",
      "time":"2013-06-21T17:51:38.063560Z",
      "bid":1.37489,
      "ask":1.37517,
      "status": "halted"                    // このレスポンスのパラメータは当該銘柄がOANDAプラットフォーム上で現在Halted(停止)状態の場合のみ設定されます。
    }
  ]
}
```

### 過去のレート一括取得
##### リクエスト
```bash
curl -X GET "http://api-sandbox.oanda.com/v1/candles?instrument=EUR_USD&count=2&candleFormat=midpoint&granularity=D&dailyAlignment=0&alignmentTimezone=America%2FNew_York"
```
##### レスポンス
```
{
  "instrument" : "EUR_USD",
  "granularity": "S5",
  "candles": [
    {
      "time": "2013-06-21T17:41:00Z",  // time in RFC3339 format
      "openMid": 1.30237,
      "highMid": 1.30237,
      "lowMid": 1.30237,
      "closeMid": 1.30237,
      "volume" : 5000,
      "complete": true
    },
    {
      "time": "2013-06-21T17:41:05Z",  // time in RFC3339 format
      "openMid": 1.30242,
      "highMid": 1.30242,
      "lowMid": 1.30242,
      "closeMid": 1.30242,
      "volume" : 2000,
      "complete": true
    }
  ]
}
```
