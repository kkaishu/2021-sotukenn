import streamlit as st
import pandas as pd
import math
import plotly.express as px
import numpy as np
from sklearn import tree
import plotly.express as px
import matplotlib as mpl
import matplotlib.pyplot as plt
import time
st.title('J2リーグ観客動員数予測プログラム')
#st.header('ヘッダー')
st.header('次の中から調べたいチーム名を下のバナーから選択してください ')
#st.write('文字列') # markdown
team_name = st.selectbox(
    '(2017~2019シーズンのJ2リーグ在籍チームに限ります。'
    '横浜FMはJ1在籍チームであるため、横浜=横浜FCです。)',
    ("愛媛","横浜","岡山","岐阜","京都","金沢","熊本","甲府","山形","山口","讃岐","鹿児島","松本","湘南","新潟","水戸","千葉","群馬","大宮","大分","町田","長崎","東京","徳島","栃木","柏","福岡","名古屋","琉球"))
latest_iteration = st.empty()
bar = st.progress(0)
for i in range(100):
    latest_iteration.text(f'{i+1}%')
    bar.progress(i+1)
    time.sleep(0.05)
st.header(f'2017~2019年シーズン　{team_name}ホームゲーム全試合データ')
team_number=team_name.replace("愛媛","37").replace("横浜","34").replace("岡山","42").replace("岐阜","39").replace("京都","24").replace("金沢","275").replace("熊本","38")\
                     .replace("甲府","28").replace("山形","29").replace("山口","330").replace("讃岐","48").replace("鹿児島","338").replace("松本","46").replace("湘南","12")\
                     .replace("新潟","78").replace("水戸","94").replace("千葉","2").replace("群馬","35").replace("大宮","27").replace("大分","31").replace("町田","45")\
                     .replace("長崎","47").replace("東京","4").replace("徳島","36").replace("栃木","40").replace("柏","11").replace("福岡","23").replace("名古屋","8").replace("琉球","277")
url=f"https://data.j-league.or.jp/SFMS01/search?competition_years=2019&competition_years=2018&competition_years=2017&competition_frame_ids=2&team_ids={team_number}&home_away_select=1&tv_relay_station_name="

fomerdata=pd.read_html(url,header=0)
data=fomerdata[0].drop(["大会","スタジアム"],axis=1)
game_day=data.試合日
game_day=[s.replace("月・祝","月").replace("火・祝","火").replace("水・祝","水").replace("木・祝","木").replace("金・祝","金")\
         .replace("土・祝","土").replace("日・祝","日").replace("月・休","月") for s in game_day]
day=data.年度.astype(str)+"/"+game_day
day=pd.DataFrame({"年/月/日":day})
data=pd.concat([data,day],axis=1)
tenki=pd.read_excel(f"c:\\Users\\梅津魁秀\\Desktop\\卒業研究\\天気データ\\全国天気\\{team_name}.xlsx",skiprows=3)
tenki=tenki.rename({"×":0})
tenki=tenki.drop(tenki.index[[0]])
day2=tenki.年.round().astype(int).astype(str)+"/"+tenki.月.round().astype(int).astype(str).str.zfill(2)+"/"+tenki.日.round().astype(int).astype(str).str.zfill(2)+"("+tenki.曜日+")"
day2=pd.DataFrame({"年/月/日":day2})
tenki=pd.concat([tenki,day2],axis=1)
data=pd.merge(data,tenki[["年/月/日","平均気温(℃)","降水量の合計(mm)","日照時間(時間)"]],on="年/月/日",how="left")
sec=data.節.str.translate(str.maketrans({chr(0xFF01 + i): chr(0x21 + i) for i in range(94)}))
sec=sec.str.extract("(.+)節",expand=True).rename(columns={0:"節数"})
data=pd.concat([data,sec],axis=1)
rank=pd.read_csv("c:\\Users\\梅津魁秀\\anaconda3\\rank.csv").drop(["Unnamed: 0"],axis=1)
rank2=rank.rename(columns={"アウェイ":"ホーム"})
data=pd.merge(data,rank[["アウェイ","節数","年度","順位"]],on=["アウェイ","年度","節数"],how="left")
data=pd.merge(data,rank2[["ホーム","節数","年度","順位"]],on=["ホーム","年度","節数"],how="left")
data=data.rename(columns={"順位_x":"アウェイ順位","順位_y":"ホーム順位"})
st.dataframe(data)
data["節数"]=data["節数"].str.replace('第', '')
data["K/O時刻"]=data["K/O時刻"].str[:2]
score=data.スコア.str.split('-', expand=True)
score=score[[0,1]].astype(np.int64)
data["点数(ホームーアウェイ)"]=score[0]-score[1]
data=data.drop(["年度","節","試合日","ホーム","インターネット中継・TV放送","年/月/日","アウェイ","スコア"],axis=1)
visitors=data.入場者数.mean()
st.header("入場者数平均(人)")
st.write(int(visitors))
plot=pd.DataFrame(data["入場者数"])
plot["入場者数平均"]=visitors
st.header('入場者数推移')
st.line_chart(plot)
data.loc[data['入場者数'] > visitors, 'large or small'] = "large"
data.loc[data['入場者数'] < visitors, 'large or small'] = "small"
large_number=data=="large"
small_number=data=="small"
st.header("largeと分類された試合数")
st.write(large_number.values.sum())
st.header("smallと分類された試合数")
st.write(small_number.values.sum())
clf = tree.DecisionTreeClassifier(max_depth = 3)
y=data['large or small'].values
x=data.drop(["入場者数","large or small"], axis=1)
clf=clf.fit(x,y)
predicted = clf.predict(x)
st.header("決定木を用いた分類")
st.subheader("分類結果")
st.write(predicted)
st.subheader("実際の分類")
st.write(y)
st.subheader("分類正答率")
st.write(sum(predicted == y) / len(x))
