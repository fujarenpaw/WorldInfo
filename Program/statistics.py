#!/usr/bin/python
# -*- Coding: utf-8 -*-
import folium
import pandas as pd

geojson = r'..\Data\worldJson\countries.geo.json'
IMF_TARGET_COL = "2019"


def main():
    IMF_data_view()


# IMFのデータにある統計情報を描画する
def IMF_data_view():
    targetCol = "target"
    legendBins = "bins"
    
    detailViwes = [
        {targetCol: 'NGDPD', legendBins: [0, 100, 2000, 4000, 6000, 8000, 10000, 15000, 22000]},
        {targetCol: 'NGDPDPC', legendBins: 8},
        {targetCol: 'NGSD_NGDP', legendBins: 8},
        {targetCol: 'PCPIPCH', legendBins: [-30, 0, 30, 60, 90, 130, 170]},
        {targetCol: 'LUR', legendBins: 8},
        {targetCol: 'GGXWDG_NGDP', legendBins: 8},
        {targetCol: 'BCA_NGDPD', legendBins: 8},
                          ]

    # IMFデータ読み込み
    path = r"..\Data\IMF_GDP_DATA_2019OCT.csv"
    df = pd.read_csv(path)

    # 不要な文字を置換
    # dataframeを一括置換では、正常に動作しなかったためforで処理
    for i in list(df.index):
        if type(df.ix[i, IMF_TARGET_COL]) is str:
            df.ix[i, IMF_TARGET_COL] = df.ix[i, IMF_TARGET_COL].replace(",", "").replace("--", "")
    # floatがたにキャスト
    df[IMF_TARGET_COL] = df[IMF_TARGET_COL].astype("float64")

    # 各データの描画
    for v in detailViwes:
        worldMapView(df, v[targetCol], v[legendBins])


# 世界地図に情報を描画する
def worldMapView(df, targetCol, bin):
    # 世界地図を作製
    m = folium.Map(location=[50, 0], zoom_start=1)
    viewData = df[df["WEO Subject Code"] == targetCol]
    viewData.reset_index(inplace=True, drop=True)
    # scaleがNanの場合はscaleを凡例に入れない
    if viewData.ix[0, "Scale"] != viewData.ix[0, "Scale"]:
        legend = viewData.ix[0, "Subject Descriptor"] + "(%s)" % (viewData.ix[0, "Units"])
    # nanではない
    else:
        legend = viewData.ix[0, "Subject Descriptor"] + "(%s %s)" % (viewData.ix[0, "Units"], viewData.ix[0, "Scale"])

    # 地図に色を塗る
    folium.Choropleth(
        geo_data=geojson,
        name='choropleth',
        data=viewData,  # 描画データ
        columns=['ISO', IMF_TARGET_COL],  # ["国コード", "値の列"]
        key_on='feature.id',
        fill_color='YlOrBr',  # 色指定
        bins=bin,  # 閾値
        fill_opacity=0.7,  # 色の透明度
        line_opacity=1,  # 国境線の透明度
        legend_name=legend  # 凡例
    ).add_to(m)
    m.save(targetCol + ".html")


if __name__ == '__main__':
    main()
