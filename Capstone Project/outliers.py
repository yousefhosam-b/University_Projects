import pandas as pd

path=""
df_d104 = pd.read_csv(path+"/d104_timeleft_CORRECT.csv", delimiter=",")
list(df_d104.columns)
df_d104 = df_d104.rename(columns = {'CuffLycra_ActualTension1_PDP': 'sensor1', 
                                    'CuffLycra_ActualTension2_PDP': 'sensor2',
                                    'CuffLycra_ActualTension3_PDP': 'sensor3', 
                                    'CuffLycra_ActualTension4_PDP': 'sensor4', 
                                    }, inplace = False)
df_d104 = df_d104.drop(['Unnamed: 0'], axis=1)
df_d104 = df_d104[(df_d104['timeLeft'] != -1)] #droping values not within breakouts range

#5262608
df = df_d104.loc[(df_d104['sensor1'] == 5262608)|
                 (df_d104['sensor2'] == 5262608)|
                 (df_d104['sensor3'] == 5262608)|
                 (df_d104['sensor4'] == 5262608)]
#14422 rows with value 5262608 TOTAL LENGTH = 355095

df_filtered = df_d104[(df_d104['sensor1'] != 5262608)|
                 (df_d104['sensor2'] != 5262608)]
df_filtered = df_d104[(df_d104['sensor3'] != 5262608)|
                 (df_d104['sensor4'] != 5262608)]

import pandas as pd
from sklearn import preprocessing
x = df_filtered[['sensor1','sensor2','sensor3','sensor4']].values 
min_max_scaler = preprocessing.MinMaxScaler()
x_scaled = min_max_scaler.fit_transform(x)
df_filtered[['sensor1','sensor2','sensor3','sensor4']] = pd.DataFrame(x_scaled).values

df["sensor1"].replace({5262608: 1}, inplace=True)
df["sensor2"].replace({5262608: 1}, inplace=True)
df["sensor3"].replace({5262608: 1}, inplace=True)
df["sensor4"].replace({5262608: 1}, inplace=True)
df = df[(df['sensor1'] <= 1) | (df['sensor2'] <= 1)]
df_d104 = df_filtered.append(df)

df_d104.sort_values("recordTimestamp")
df_d104.to_csv("d104.csv")


          