import pandas as pd
path=""
df = pd.read_csv(path+"/d104.csv", delimiter=",")
df = df[df.columns[2:]]

df_breakouts = df[df['timeLeft'] <= 3600]

df_b1 = df.loc[51807    :52557]
df_b2 = df.loc[65768    :66512]
df_b3 = df.loc[66513    :67055]
df_b4 = df.loc[67056    :67152]
df_b5 = df.loc[81874    :82673]
df_b6 = df.loc[83359    :84175]
df_b7 = df.loc[318914   :319699]
df_b8 = df.loc[324109   :324904]
df_b9 = df.loc[327373   :328153]
df_b10 = df.loc[334523  :335254]
df_b11 = df.loc[339941  :340672]
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
    
    sensormin = df_b1[df_b.columns[1:4,]].min()
    sensormax = df_b1[df_b.columns[1:4,]].max()
    plt.ylim([sensormin,sensormax])
    rtmin = df_b['recordTimestamp'].min()
    rtmax = df_b['recordTimestamp'].max()
    plt.xlim([rtmin,rtmax])
    breakoutTime = df_b[df_b['timeLeft']==0]['recordTimestamp']
    plt.axvspan(breakoutTime.min(),breakoutTime.max(), color='gray', alpha=0.5)
    for col in df_b.columns[1:5,]:
        y = df_b[col]
        x=df_b['recordTimestamp']
        plt.plot(x,y)
    
    fig = plt.gcf()
    fig.set_size_inches(100, 25,forward=True)
    fig.savefig('breakout{}.png'.format(counter), dpi=100)
    # show a legend on the plot
    plt.legend(df_b.columns[1:5,])
    # Display a figure.
    plt.show()
    counter+=1



