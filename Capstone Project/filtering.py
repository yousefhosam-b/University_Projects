import pandas as pd
import numpy as np

# load or create your dataset
path=""
df = pd.read_csv(path+"/d104.csv", delimiter=",")
df_filter = df.iloc[:,2:]
df_filter["filterWarning"]=False
print(df_filter.columns)

print(df['C_PROFICY_ConverterDTStartEnd'].value_counts().head())
#most frequent values
for colName in df_filter.iloc[:,1:5].columns:
    print("ALL VALUES")
    print(df_filter[colName].value_counts().head())
    print("===========================")
    print("VALUES WHILE MACHINE IS WORKING")
    print(df.loc[df['C_PROFICY_ConverterDTStartEnd'] == 0][colName].value_counts().head())
    print("===========================")
    df.hist(column=colName)
    df_filter[colName] = df_filter[colName].rolling(5,min_periods=1).mean().values


s1 = 0.81
s2 = 0.61
s3 = 0.76
s4 = 0.65
for percentage in [0.2]:
    for index, row in df_filter.iterrows():
        if(s1*(1-percentage)<row['sensor1']<s1*(1+percentage) and
        s2*(1-percentage)<row['sensor2']<s2*(1+percentage) and
        s3*(1-percentage)<row['sensor3']<s3*(1+percentage) and
        s4*(1-percentage)<row['sensor4']<s4*(1+percentage)):
            df_filter.loc[index, 'filterWarning'] = False
        else:
            df_filter.loc[index, 'filterWarning'] = True
    print(f"{percentage} freedom")
    print("Machine Working")
    print(df_filter.loc[df['C_PROFICY_ConverterDTStartEnd'] == 0]['filterWarning'].value_counts())
    print("Machine NOT Working")
    print(df_filter.loc[df['C_PROFICY_ConverterDTStartEnd'] != 0]['filterWarning'].value_counts())
    print("======================================================")

df_6000 = df_filter[df_filter['timeLeft']<6000]

def getTPFPTNFN(y_true, y_pred):
    TP, FP, TN, FN = 0, 0, 0, 0
    for s_true, s_pred in zip (y_true, y_pred):
        if s_true <= 1800:
            if s_pred == True:
                TP += 1
            else:
                FN += 1
        else:
            if s_pred == False:
                TN += 1
            else:
                FP += 1
                
    print(f"True Positive:{TP}\nFalse Positive:{FP}\nTrue Negative:{TN}\nFalse Negative:{FN}")
    return TP, FP, TN, FN

getTPFPTNFN(df_filter['timeLeft'], df_filter['filterWarning'])

df_b1 = df_filter.loc[51807    :52557+600,]
df_b2 = df_filter.loc[65768    :66512+600,]
df_b3 = df_filter.loc[66513    :67055+600,]
df_b4 = df_filter.loc[67056    :67152+600,]
df_b5 = df_filter.loc[81874    :82673+600,]
df_b6 = df_filter.loc[83359    :84175+600,]
df_b7 = df_filter.loc[318914   :319699+600,]
df_b8 = df_filter.loc[324109   :324904+600,]
df_b9 = df_filter.loc[327373   :328153+600,]
df_b10 = df_filter.loc[334523  :335254+600,]
df_b11 = df_filter.loc[339941  :340672+600,]
df_list = list([df_b1,df_b2,df_b3,df_b4,df_b5,df_b6,df_b7,df_b8,df_b9,df_b10,df_b11])

import matplotlib.pyplot as plt
import matplotlib as mpl
counter = 1
for df_b in df_list:
    mpl.rcParams['agg.path.chunksize'] = 10000
    plt.figure()
    plt.xlabel('Time',fontsize=40)
    # Set the y axis label of the current axis.
    plt.ylabel('Sensor Value',fontsize=40)
    # Set a title of the current axes.
    plt.title('Sensor Values during Breakout {}'.format(counter) ,fontsize=80)
    
    #sensormin = df_b1[df_b.columns[1:4,]].min()
    #sensormax = df_b1[df_b.columns[1:4,]].max()
    #plt.ylim([sensormin,sensormax])
    #rtmin = df_b['recordTimestamp'].min()
    #rtmax = df_b['recordTimestamp'].max()
    #plt.xlim([rtmin,rtmax])
    breakoutTime = df_b[df_b['timeLeft']==0]['recordTimestamp']
    plt.axvspan(breakoutTime.min(),breakoutTime.max(), color='gray', alpha=0.5)
    for col in df_b.columns[1:5,]:
        y = df_b[col]
        x=df_b['recordTimestamp']
        plt.plot(x,y)
        plt.plot(x,df_b['filterWarning'],scaley=True,color="lime")
    
    fig = plt.gcf()
    fig.set_size_inches(100, 25,forward=True)
    fig.savefig('breakout{}.png'.format(counter), dpi=100)
    # show a legend on the plot
    plt.legend(df_b.columns[1:5,])
    # Display a figure.
    plt.show()
    counter+=1





import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.rcParams['agg.path.chunksize'] = 10000
plt.figure()
plt.xlabel('Time',fontsize=40)
# Set the y axis label of the current axis.
plt.ylabel('Sensor Value',fontsize=40)
# Set a title of the current axes.
plt.title("Sensor Values during Breakouts",fontsize=80)

#sensormin = df_b1[df_b.columns[1:4,]].min()
#sensormax = df_b1[df_b.columns[1:4,]].max()
#plt.ylim([sensormin,sensormax])
#rtmin = df_b['recordTimestamp'].min()
#rtmax = df_b['recordTimestamp'].max()
#plt.xlim([rtmin,rtmax])
breakouts = df_filter[df_filter['timeLeft']<1]['recordTimestamp']
for xc in breakouts:
    plt.axvline(x=xc, color='lime', linestyle='--')
for col in df_filter.columns[1:5,]:
    y = df_filter[df_filter['timeLeft']<3600][col]
    x=  df_filter[df_filter['timeLeft']<3600]['recordTimestamp']
    plt.scatter(x,y)

fig = plt.gcf()
fig.set_size_inches(500, 10,forward=True)
#fig.savefig('breakout{}.png'.format(counter), dpi=100)
# show a legend on the plot
plt.legend(df_filter.columns[1:5,])
# Display a figure.
plt.show()

