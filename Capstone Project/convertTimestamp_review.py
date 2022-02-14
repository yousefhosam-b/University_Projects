import py7zr

archive = py7zr.SevenZipFile('RawData.7z', mode='r')
archive.extractall(path="")
archive.close()

#Files : D104_15 Dec , D106_15 Dec
path=""

import pandas as pd

df_d104 = pd.read_csv(path+"/D104_15 Dec.csv", delimiter=",")

for col in df_d104.columns: 
    print(col)

colNames_timestamp = ["CuffLycra_ActualTension1_PDP_timestamp",
                      "CuffLycra_ActualTension2_PDP_timestamp",
                      "CuffLycra_ActualTension3_PDP_timestamp",
                      "CuffLycra_ActualTension4_PDP_timestamp"]

print(df_d104.duplicated(subset=colNames_timestamp).sum())

def getDuplicateColumns(df): 
  
    # Create an empty set 
    duplicateColumnNames = set() 
      
    # Iterate through all the columns of dataframe 
    for x in range(df.shape[1]): 
          
        # Take column at xth index. 
        col = df.iloc[:, x] 
          
        # Iterate through all the columns in DataFrame from (x + 1)th index to last index 
        for y in range(x + 1, df.shape[1]): 
              
            # Take column at yth index. 
            otherCol = df.iloc[:, y] 
              
            # Check if two columns at x & y index are equal or not, if equal then adding to the set 
            if col.equals(otherCol):
                duplicateColumnNames.add(df.columns.values[x]) 
                duplicateColumnNames.add(df.columns.values[y]) 
                  
    # Return list of unique column names whose contents are duplicates. 
    return list(duplicateColumnNames)

print(getDuplicateColumns(df_d104[colNames_timestamp]))

'''
Out of 540515 lines 108809 lines have the same timestamp since there are many ones with different timestamps
it is suggested to keep duplicated timestamps since its impossible to delete colums due to ~400000 different valued timestamps

in all of the dataframe it seems like
['CuffLycra_SetpointStream3_PDP_timestamp', 'CuffLycra_ActualTension1_PDP_timestamp', 
 'CuffLycra_SetpointStream4_PDP_timestamp', 'CuffLycra_ActualTension2_PDP_timestamp']
are the same so they are more likely to be duplicated
'''

from datetime import datetime
df_timestamp = df_d104[colNames_timestamp]
print(type(df_timestamp))

"""
Here im cheking for the first colomn of each row with other columns for duplicated value
"""
for index, row in df_timestamp.iterrows():
    value = row[0]
    for colon in colNames_timestamp[1:]:
        if(row[colon] == value):
            df_timestamp[colon][index] = 0

"""
There are 10298 items that change timestamps
Here im converting timestamps
"""
from tqdm import tqdm
for index, row in tqdm(df_timestamp.iterrows()):
    for colon in colNames_timestamp:
       if(row[colon]!=0):
           print(row[colon])
           itemstr = str(row[colon])
           itemstr = itemstr[:-3]
           itemint = int(itemstr)
           value = row[colon]
           df_timestamp[colon][index] = datetime.fromtimestamp(itemint)
        
df_timestamp.to_csv("timestampsD104.csv")

import pandas as pd
df = pd.read_csv("timestampsD104.csv", delimiter=",")

from tqdm import tqdm
for index, row in tqdm(df.iterrows()):
        colon = 'recordTimestamp'
        print(row[colon])
        itemstr = str(row[colon])
        itemstr = itemstr[:-3]
        itemint = int(itemstr)
        df[colon][index] = datetime.fromtimestamp(itemint)
        
df.to_csv("timestampsD104recordTimesteam.csv")

for column in df_timestamp:
    for item in df_timestamp[column]:
       itemstr = str(item)
       itemstr = itemstr[:-3]
       itemint = int(itemstr)
       
       #df_timestamp[column][item] = itemdate

for column in colNames_timestamp:
    df_d104[column]=df_timestamp[column]

df_d104.to_csv("timestampsD104.csv")

timestamp_repetition = df.pivot_table(index=["CuffLycra_SetpointStream1_PDP_timestamp"], aggfunc='size')
timestamp_repetition = timestamp_repetition[timestamp_repetition != 1]


import pandas as pd
from datetime import datetime
df = pd.read_csv("timestampsD104recordTimestamp.csv", delimiter=",")


df_sorted = df.sort_values(['recordTimestamp'])
df_breakouts = pd.DataFrame(columns= df_sorted.columns)
df_sorted['recordTimestamp'] = pd.to_datetime(df_sorted.recordTimestamp)


#VISUALIZATION
import matplotlib.pyplot as plt

df = pd.read_csv(path+"/timestampsD104.csv", delimiter=",")


data = [df.CuffLycra_ActualTension1_PDP,
        df.CuffLycra_ActualTension2_PDP,
        df.CuffLycra_ActualTension3_PDP,
        df.CuffLycra_ActualTension4_PDP,]


#Boxplot
fig1, ax1 = plt.subplots()
ax1.set_title('Box Plot For Sensors')
ax1.set_xticklabels(['ActualTension1','ActualTension2','ActualTension3','ActualTension4'], rotation = 270)
ax1.set_ylim(0, 260)
plt.figure(figsize=(6,3))
ax1.boxplot(data)
box1 = plt.boxplot(data, notch=True, patch_artist=True)
for item in ['boxes', 'whiskers', 'fliers', 'medians', 'caps']:
        plt.setp(box1[item], color='black')
plt.setp(box1["boxes"], facecolor='y')
plt.setp(box1["fliers"], markeredgecolor='black')
plt.xticks([1,2,3,4],['ActualTension1','ActualTension2','ActualTension3','ActualTension4'], rotation = 270)
plt.xlim(0.5,4.5)
plt.ylim(-5, 260)
plt.title('Actual Tension Sensors')
plt.show()

#Duration of breakouts
df_err_breakouts = pd.read_csv(path+"\Breakout.csv", sheet_name=None).get('Sayfa1')
df_differences = df_err_breakouts['End Time'] - df_err_breakouts['Start Time']
df_differences = df_differences.astype('timedelta64[s]')
plt.bar(df_differences.index, df_differences, align='center', alpha=0.5)
plt.ylabel('Duration Time(seconds)')
plt.xlabel('Breakouts')
plt.title('Breakout Durations')

#Heatmap for D104 data
import matplotlib.pyplot as plt 
import seaborn as sb
corr = df.corr()
plt.figure(figsize = (20, 10))
a = sb.heatmap(corr, annot = True, fmt = '.2f')
a.set_ylim(0, 10)

#Heatmap for breakouts dataframe
import matplotlib.pyplot as plt 
import seaborn as sb
corr = df_breakouts.corr()
plt.figure(figsize = (20, 10))
a = sb.heatmap(corr, annot = True, fmt = '.2f')
a.set_ylim(0, 10)

