import pandas as pd
import numpy as np

path = ""    
# import data
df_d104 = pd.read_csv(path+"/d104_timeleft_CORRECT.csv", delimiter=",")

#drop data
df_d104.drop(df_d104[df_d104['timeLeft']<0].index, inplace = True)
df_d104.drop(df_d104[df_d104['CuffLycra_ActualTension1_PDP']<5000].index, inplace = True)
df_d104.drop(df_d104[df_d104['CuffLycra_ActualTension2_PDP']<5000].index, inplace = True)
df_d104.drop(df_d104[df_d104['CuffLycra_ActualTension3_PDP']<5000].index, inplace = True)
df_d104.drop(df_d104[df_d104['CuffLycra_ActualTension4_PDP']<5000].index, inplace = True)
#355095:540514


# NORMALIZATION ActualTension1,2,3,4
from sklearn import preprocessing
y = df_d104.iloc[:,5]
normalized_arr = preprocessing.normalize([y])
print(normalized_arr)
from sklearn.preprocessing import MinMaxScaler
norm = MinMaxScaler().fit(y.values.reshape(-1,1))
normalized = norm.transform(y.values.reshape(-1,1))
rounding = np.round(normalized)
df_d104['CuffLycra_ActualTension4_PDP'] = rounding

df_d104['CuffLycra_ActualTension4_PDP'] = df_d104['CuffLycra_ActualTension4_PDP'].replace(0, 1)


df = df_d104
# Change values to 1
from sklearn import preprocessing
col_mean = df_d104['CuffLycra_ActualTension1_PDP']

y = df_d104.iloc[:,2]
df_d104 = df_d104.replace(y, "1") 

df_d104['CuffLycra_ActualTension1_PDP'] = rounding

df_d104Norm=df_d104.append([df_d104,df])
df_d104Norm = [df_d104, df]

df_d104Norm.to_csv("Normalized_D104.csv")
