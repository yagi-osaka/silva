import pandas as pd
import datetime

def __table__(df_pre,df,i,label_unit):
    label = label_unit[i]
    df_e = df[df['field.name'].str.contains(label)]
    df_e = df_e.drop(['%time','field.header.seq','field.header.frame_id','field.name','field.seq','field.msgid'],axis='columns')
    df_e = df_e.rename(columns={'field.header.stamp':label+' time', 'field.payload0':'joint'+str(5*i), 'field.payload1':'joint'+str(5*i+1), 'field.payload2':'joint'+str(5*i+2), 'field.payload3':'joint'+str(5*i+3), 'field.payload4':'joint'+str(5*i+4)})
    df_e = df_e.reset_index(drop=True)
    df_e[label+' time'] = df_e[label+' time']*0.000000001+3600*9
    for j in range(0,5):
        df_e['joint'+str(5*i+j)] = df_e['joint'+str(5*i+j)]*0.1
    df_e[label+' time'] = pd.to_datetime(df_e[label+' time'],unit='s')
    df_e = pd.concat([df_e,df_pre],axis=1)
    if i==0:
        return df_e
    else: return __table__(df_e,df,i-1,label_unit)

df = pd.read_csv('yagi.csv') #読み込むファイル名
i = 6 #読み込むノード数-1
label_unit = ['hip','arml','armr','neck','headl','headr','headc'] #ノードのラベル名

df_pre = pd.DataFrame()
df = __table__(df_pre, df, i, label_unit)
#print(df)
df.to_csv("yagi2.csv") #出力したいファイル名
