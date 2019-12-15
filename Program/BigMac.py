import pandas as pd
import folium
# Economistが公開しているビッグマック指数のデータを読み込み
url = "https://github.com/TheEconomist/big-mac-data/blob/master/output-data/big-mac-full-index.csv"
df = pd.read_html(url, header=0)[0]

# 1つの国で日付の異なる複数のデータがあるため、古い重複データは削除
df = df.drop_duplicates(['iso_a3'], keep='last')

# 世界地図を作製
m = folium.Map(location=[50, 0], zoom_start=1)

#geojson = 'https://github.com/johan/world.geo.json/blob/master/countries.geo.json'
geojson = r'..\Data\worldJson\countries.geo.json'
# 地図に色を塗る
folium.Choropleth(
    geo_data=geojson,
    name='choropleth',
    data=df,# 描画データ
    columns=['iso_a3', 'dollar_price'], # ["国コード", "値の列"]
    key_on='feature.id',
    fill_color='OrRd',# 色指定
    fill_opacity=0.7,    # 色の透明度
    line_opacity=1,#国境線の透明度
    legend_name='big mac index dollar_price' #凡例
).add_to(m)

m.save("world.html")
