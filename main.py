import numpy as np
import pandas as pd
import pdfplumber as pdfp
import locale
from locale import atof

def pagina2(data):

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
def pagina3(data):
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
    fin = tst2.replace(r'\n','', regex=True)
    fin.to_csv("pagina3.csv",index=False,na_rep="Nan")


##### Pagina 16 document #####
def pagina16(data):
    pagina16 = data.pages[15]

    crop_A = pagina16.within_bbox((0,50, pagina16.width,310))
    cA=crop_A.to_image(resolution=150)

    crop_B = pagina16.within_bbox((0,310, pagina16.width,460))
    cB =crop_B.to_image(resolution=150)

    crop_C = pagina16.within_bbox((0,470, pagina16.width,650))
    CC=crop_C.to_image(resolution=150)

    table_settings={
        "vertical_strategy":"text",
        "horizontal_strategy":"text",
        # "text_keep_blank_chars":True,
        "snap_y_tolerance":6,
        "intersection_x_tolerance":10,
        "explicit_vertical_lines":[35]
        }
    
    cols =["3Q23 ","4Q23 ","1Q24 ","2Q24 ","3Q24 ","4Q24 ","1Q25 ","2Q25 ","3Q25 ","4Q25 "]
    table16a=crop_A.extract_table(table_settings)
    nova =[]
    for x in table16a:
        aux = [''.join(x[0:2])]
        x =aux+x[2:]
        nova.append(x)
    Anet = pd.DataFrame(nova[1:], columns=nova[0])
    Anet = Anet.replace(r' ','', regex=True)
    Anet.to_csv("pg16A.csv",index=False)

    table16b=crop_B.extract_table(table_settings)
    nova =[]
    for x in table16b:
        aux = [''.join(x[0:2])]
        x =aux+x[2:]
        nova.append(x)
    Bnet = pd.DataFrame(nova[1:], columns=nova[0])
    Bnet = Bnet.replace(r' ','', regex=True)
    for x in cols:
        Bnet[x]=pd.to_numeric(Bnet[x],errors="ignore")
    Bnet.to_csv("pg16B.csv",index=False)

    table16c=crop_B.extract_table(table_settings)
    nova =[]
    for x in table16c:
        aux = [''.join(x[0:2])]
        x =aux+x[2:]
        nova.append(x)
    Cnet = pd.DataFrame(nova[1:], columns=nova[0])
    Cnet = Cnet.replace(r' ','', regex=True)
    for x in cols:
        Cnet[x]=pd.to_numeric(Cnet[x],errors="ignore") 
    Cnet.to_csv("pg16C.csv",index=False)

def pagina17(data):
    pagina17 = data.pages[16]

    table_settings={
        "vertical_strategy":"text",
        "horizontal_strategy":"lines"
        }

    table17 = pagina17.extract_table(table_settings)
    columnes = table17[0]
    columnes[0]="Paisos/factors"
    df17 = pd.DataFrame(table17[2:],columns=columnes)
    df17.columns
    for x in columnes:
        df17[x]=pd.to_numeric(df17[x],errors="ignore")
    df17.to_csv("pagina17.csv",index=False)


def main():
    data = pdfp.open("241025 Unicredit Macro & Markets Weekly Focus - python.pdf")

    pagina2(data)
    pagina3(data)
    pagina16(data)
    pagina17(data)


if __name__=="__main__":
    main()