#!/usr/bin/python
# -*- Coding: utf-8 -*-
import http.client
import json
import datetime
import pandas as pd
import time

conn = http.client.HTTPSConnection("skyscanner-skyscanner-flight-search-v1.p.rapidapi.com")
headers = {
    'x-rapidapi-host': "skyscanner-skyscanner-flight-search-v1.p.rapidapi.com",
    'x-rapidapi-key': "****"
}

# AIRPORT CODE
NARITA_AIRPORT = "NRT-sky"
NAHA_AIRPORT = "OKA-sky"
CAIRNS_AIRPORT = "CNS-sky"
MELBOURNE_AIRPORT = "MEL-sky"
PERTH_AIRPORT = "PER-sky"
SYDNEY_AIRPORT = "SYD-sky"

DAYS = 365
DATE_COL = "Date"
OUTWARD_COL = "Outward"
RETURN_TRIP_COL = "Return"


def main():
    # getAirFare(NARITA_AIRPORT, NAHA_AIRPORT)
    getAirFare(NARITA_AIRPORT, CAIRNS_AIRPORT)
    getAirFare(NARITA_AIRPORT, MELBOURNE_AIRPORT)
    getAirFare(NARITA_AIRPORT, PERTH_AIRPORT)
    getAirFare(NARITA_AIRPORT, SYDNEY_AIRPORT)


# 出発空港コード:departureAirportCode
# 到着空港コード:arrivalAirportCode
def getAirFare(departureAirportCode, arrivalAirportCode):
    # 価格格納用データフレーム生成
    data = pd.DataFrame(index=range(DAYS), columns=[DATE_COL, OUTWARD_COL, RETURN_TRIP_COL])

    # 基準日
    date = datetime.datetime(2020, 1, 15)
    # 基準日 + DAYS日間の最安値を取得する
    for i in range(DAYS):
        print(date.strftime('%Y-%m-%d'))
        # データ取得
        data.ix[i, DATE_COL] = date
        # 往路
        data.ix[i, OUTWARD_COL] = getMinPrice(departureAirportCode, arrivalAirportCode, date.strftime('%Y-%m-%d'))
        # 復路
        data.ix[i, RETURN_TRIP_COL] = getMinPrice(arrivalAirportCode, departureAirportCode, date.strftime('%Y-%m-%d'))

        # 1日進める
        date += datetime.timedelta(days=1)

        if i % 50 == 0:
            data.to_csv(arrivalAirportCode + ".csv")

    data.to_csv(arrivalAirportCode + ".csv")


# 最安値を取得する
def getMinPrice(originplace, destinationplace, outboundpartialdate):
    # API呼び出しに余裕を持たせないと値を取れない事があったため、3秒待つ
    time.sleep(3)

    # APIに問い合わせ
    conn.request("GET", "/apiservices/browsequotes/v1.0/JP/JPY/ja-JP/%s/%s/%s" % (originplace, destinationplace, outboundpartialdate), headers=headers)
    res = conn.getresponse()
    data = res.read()
    # json形式のレスポンスのため、jsonとしてロードする
    js = json.loads(data.decode("utf-8"))

    # 正常に最低値を受け取れていない場合は、Noneを返す
    try:
        return int(js['Quotes'][0]['MinPrice'])
    except (IndexError, KeyError):
        return None


if __name__ == '__main__':
    main()
