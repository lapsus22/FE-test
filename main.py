import numpy as np
import pandas as pd
import pdfplumber as pdfp
import locale
from locale import atof
data = pdfp.open("241025 Unicredit Macro & Markets Weekly Focus - python.pdf")

table_settings={
    "vertical_strategy":"text",
    "horizontal_strategy":"text",
    "text_keep_blank_chars":True,
    "text_y_tolerance":5,
    "snap_y_tolerance":5

}
pagina = data.pages[1]
table=pagina.extract_table(table_settings)
table[0]=["Name","Current","1M","3M","6M","12M","YTD","QTD"]
df = pd.DataFrame(table[1:],columns=table[0])

#teball pagina 2
new_data = df.drop([0,8,9,16,17,26,27,28,32,33])
columns = ["Current","1M","3M","6M","12M","YTD","QTD"]
for x in columns:
    new_data[x]=pd.to_numeric(new_data[x],errors="ignore")

locale.setlocale(locale.LC_NUMERIC, '')
new_data["Current"]=new_data["Current"].map(atof)

# average results
average = ["average","NaN"]
cols =["1M","3M","6M","12M","YTD","QTD"]
for x in cols:
    average.append(new_data[x].mean()) 
aux = pd.DataFrame([average], columns=["Name","Current","1M","3M","6M","12M","YTD","QTD"]) 
test = pd.concat([new_data,aux])
test.to_csv("pagina2.csv",index=False)

#Top i bot perfoming indexes a t 12M
dates12 = new_data[["Name","12M"]]
top =dates12.sort_values(by="12M",ascending=False)
top3 = top[:3].reset_index()
top3.drop("index", axis=1, inplace=True)
top3.to_csv("top3.csv")
bot = dates12.sort_values(by="12M")
bot3 = bot[:3].reset_index()
bot3.drop("index", axis=1, inplace=True)
bot3.to_csv("bot3.csv")



##### Pagina 3 document #####

pg_2 = data.pages[2]
table_settings2={
    "vertical_strategy":"text",
    "horizontal_strategy":"lines",
    "text_keep_blank_chars":True,

}

table_2=pg_2.extract_table(table_settings2)
table_2[0]=["Date 26 oct - 01 Nov 2024","Time (CET)","Country","Indicator/Event","Period","UniCredit estimates","Consensus (Bloomberg)","Previous"]
df2 = pd.DataFrame(table_2[2:], columns=table_2[0])
columns = ["UniCredit estimates","Consensus (Bloomberg)","Previous"]
for x in columns:
    df2[x]=pd.to_numeric(df2[x],errors="ignore")
tst2 = df2.replace(r'^\s*$', np.nan, regex=True)
tst2 = tst2.replace(r'\n','', regex=True)
tst2.to_csv("pagina3.csv",index=False)


