import py7zr

path = ""
    
path_data = ""    

archive = py7zr.SevenZipFile('Raw Data.7z','r')
archive.extractall(path)
archive.close()

# Files : D104_15 Dec , D106_15 Dec
import pandas as pd # noqa
df_d104 = pd.read_csv(path+"\D104_15 Dec.csv", delimiter=",")

"""
for col in df_d104.columns: 
    print(col)
"""
colNames_timestamp = ["CuffLycra_SetpointStream1_PDP_timestamp",
                      "CuffLycra_SetpointStream2_PDP_timestamp",
                      "CuffLycra_SetpointStream3_PDP_timestamp",
                      "CuffLycra_SetpointStream4_PDP_timestamp",
                      "CuffLycra_ActualTension1_PDP_timestamp",
                      "CuffLycra_ActualTension2_PDP_timestamp",
                      "CuffLycra_ActualTension3_PDP_timestamp",
                      "CuffLycra_ActualTension4_PDP_timestamp"]

print(df_d104.duplicated(subset=colNames_timestamp).sum())

"""
def getDuplicateColumns(df): 
  
    # Create an empty set 
    duplicateColumnNames = set() 
      
    # Iterate through all the columns  
    # of dataframe 
    for x in range(df.shape[1]): 
          
        # Take column at xth index. 
        col = df.iloc[:, x] 
          
        # Iterate through all the columns in 
        # DataFrame from (x + 1)th index to 
        # last index 
        for y in range(x + 1, df.shape[1]): 
              
            # Take column at yth index. 
            otherCol = df.iloc[:, y] 
              
            # Check if two columns at x & y 
            # index are equal or not, 
            # if equal then adding  
            # to the set 
            if col.equals(otherCol):
                duplicateColumnNames.add(df.columns.values[x]) 
                duplicateColumnNames.add(df.columns.values[y]) 
                  
    # Return list of unique column names  
    # whose contents are duplicates. 
    return list(duplicateColumnNames)

print(getDuplicateColumns(df_d104[colNames_timestamp]))

Out of 540515 lines 108809 lines have the same timestamp since there are many ones
with different timestamps it is suggested to keep duplicated timestamps since its 
impossible to delete columns due to ~400000 different valued timestamps

in all of the dataframe it seems like
['CuffLycra_SetpointStream3_PDP_timestamp', 'CuffLycra_ActualTension1_PDP_timestamp', 
 'CuffLycra_SetpointStream4_PDP_timestamp', 'CuffLycra_ActualTension2_PDP_timestamp']
are the same so they are more likely to be duplicated
"""

from datetime import datetime # noqa
df_timestamp = df_d104[colNames_timestamp]
print(type(df_timestamp))

"""
Here im checking for the first column of each row with other columns for duplicated value
"""
for index, row in df_timestamp.iterrows():
    value = row[0]
    for colon in colNames_timestamp[1:]:
        if row[colon] == value:
            df_timestamp[colon][index] = 0


"""
There are 10298 items that change timestamps
Here im converting timestamps
"""
from tqdm import tqdm # noqa
for index, row in tqdm(df_timestamp.iterrows()):
    for colon in colNames_timestamp:
        if row[colon] != 0:
            print(row[colon])
            itemstr = str(row[colon])
            itemstr = itemstr[:-3]
            itemint = int(itemstr)
            value = row[colon]
            df_timestamp[colon][index] = datetime.fromtimestamp(itemint)

df_timestamp.to_csv("timestampsD104.csv")

import pandas as pd # noqa
df = pd.read_csv("timestampsD104.csv", delimiter=",")

from tqdm import tqdm # noqa
for index, row in tqdm(df.iterrows()):
    colon = 'recordTimestamp'
    print(row[colon])
    itemstr = str(row[colon])
    itemstr = itemstr[:-3]
    itemint = int(itemstr)
    df[colon][index] = datetime.fromtimestamp(itemint)

#df.to_csv("timestampsD104recordTimesteam.csv")

"""
for column in df_timestamp:
    for item in df_timestamp[column]:
       itemstr = str(item)
       itemstr = itemstr[:-3]
       itemint = int(itemstr)
       
       df_timestamp[column][item] = itemdate

"""

for column in colNames_timestamp:
    df_d104[column] = df_timestamp[column]

#df_d104.to_csv("timestampsD104.csv")

timestamp_repetition = df.pivot_table(index=["CuffLycra_SetpointStream1_PDP_timestamp"], aggfunc='size')
timestamp_repetition = timestamp_repetition[timestamp_repetition != 1]

# new 14 01 2020 ====================================================================

import pandas as pd # noqa
from datetime import datetime # noqa
path = ""    

df = pd.read_csv("timestampsD104.csv")

df_elastic = pd.read_excel(path+"\elasticBreakout.xlsx", sheet_name=None).get('Sayfa1')

df_sorted = df.sort_values(['recordTimestamp'])
df_breakouts = pd.DataFrame(columns=df_sorted.columns)
df_sorted['recordTimestamp'] = pd.to_datetime(df_sorted.recordTimestamp)


from datetime import datetime # noqa
from datetime import timedelta # noqa
for index_elastic, row_elastic in df_elastic.iterrows():
    colon = 'recordTimestamp'
    startTime = row_elastic['Start Time'] - timedelta(seconds=300)
    endTime = row_elastic['End Time'] + timedelta(seconds=300)
    mask = (df_sorted[colon] >= startTime) & (df_sorted[colon] <= endTime)
    df_breakouts = pd.concat([df_breakouts, df_sorted.loc[mask]])
    df_new = df_breakouts

#df_breakouts.to_csv("d104_breakout_5mins.csv")
#df_breakouts.to_excel("d104_breakout_5mins.xlsx")


# PART 2 CORRELATION
df_breakouts = pd.read_excel(path+"/d104_breakout_5mins.xlsx")
columns = ['C_PROFICY_ConverterDTStartEnd',
           'CuffLycra_SetpointStream1_PDP',
           'CuffLycra_SetpointStream2_PDP',
           'CuffLycra_SetpointStream3_PDP',
           'CuffLycra_SetpointStream4_PDP',
           'CuffLycra_ActualTension1_PDP',
           'CuffLycra_ActualTension2_PDP',
           'CuffLycra_ActualTension3_PDP',
           'CuffLycra_ActualTension4_PDP']
df_breakouts = df_breakouts[columns]

for col in columns:
    unique = df_breakouts[col].unique()
    unique.sort()
    print(f"Unique values in {col}:\n{unique}")

# HEATMAP
import matplotlib.pyplot as plt # noqa
import seaborn as sb # noqa
corr = df_breakouts.corr()
plt.figure(figsize=(20, 10))
a = sb.heatmap(corr, annot=True, fmt='.2f')
a.set_ylim(0, 10)


import scipy.stats as stats # noqa

for col in columns[1:]:
    r, p = stats.pearsonr(df_breakouts[col], df_breakouts['C_PROFICY_ConverterDTStartEnd'])
    print(f"Scipy computed between {col} and C_PROFICY_ConverterDTStartEnd \nPearson r: {r} and p-value: {p}\n")


# VISUALIZATION

#SENSORS VALUES 
plt.clf()
import matplotlib.pyplot as plt # noqa
df_breakouts = pd.read_excel(path+"/d104_breakout_5mins.xlsx")
columns = ['recordTimestamp',
           'CuffLycra_ActualTension1_PDP',
           'CuffLycra_ActualTension2_PDP',
           'CuffLycra_ActualTension3_PDP',
           'CuffLycra_ActualTension4_PDP']
df_breakouts = df_breakouts[columns]
df_breakouts.plot('recordTimestamp', 'CuffLycra_ActualTension1_PDP', title='stretched_plot', figsize=(50, 2))

for col in columns[1:]:
    df_breakouts.plot('recordTimestamp', col, title='stretched_plot', figsize=(50, 2))
    plt.show()
    plt.clf()
    
'''
for col in columns[1:]:
    y = df_breakouts[col]
    x = df_breakouts['recordTimestamp']
    df = pd.DataFrame(y, index=x)
    df.plot(title='stretched_plot', figsize=(50, 1))
    # plotting the line 1 points 

plt.xlabel('Time')
# Set the y axis label of the current axis.
plt.ylabel('Value')
# Set a title of the current axes.
plt.title('Sensor Values during breakouts')
# show a legend on the plot
plt.legend()
# Display a figure.
plt.show()
'''

# WHY WE WILL MODEL?
#df_breakouts.to_excel("d104_breakout_5mins_cleared.xlsx")
df_breakouts.recordTimestamp = pd.to_datetime(df_breakouts.recordTimestamp)
df_breakouts[columns].plot('recordTimestamp', title='stretched_plot', figsize=(50, 10))
print(df_elastic['Start Time'].iloc[1])
from datetime import datetime # noqa
from datetime import timedelta # noqa
colon = 'recordTimestamp'
startTime = df_elastic['Start Time'].iloc[1] - timedelta(seconds=300)
endTime = df_elastic['End Time'].iloc[1] + timedelta(seconds=300)
mask = (df_breakouts[colon] >= startTime) & (df_breakouts[colon] <= endTime)
df_plot = df_breakouts.loc[mask]

# new 19 02 2020 ====================================================================

path = ""    


import pandas as pd 
df = pd.read_csv(path+"/timestampsD104.csv", delimiter=",")
df_breakouts = pd.read_excel(path+"/d104_breakout_5mins.xlsx")

columns = ['CuffLycra_ActualTension1_PDP',
           'CuffLycra_ActualTension2_PDP',
           'CuffLycra_ActualTension3_PDP',
           'CuffLycra_ActualTension4_PDP']

data = [df.CuffLycra_ActualTension1_PDP,
        df.CuffLycra_ActualTension2_PDP,
        df.CuffLycra_ActualTension3_PDP,
        df.CuffLycra_ActualTension4_PDP,
        df_breakouts.CuffLycra_ActualTension1_PDP,
        df_breakouts.CuffLycra_ActualTension2_PDP,
        df_breakouts.CuffLycra_ActualTension3_PDP,
        df_breakouts.CuffLycra_ActualTension4_PDP]

import matplotlib.pyplot as plt 
import matplotlib.patches as mpatches
#Boxplot
fig1, ax1 = plt.subplots()
ax1.set_title('Box Plot For Sensors')
ax1.set_xticklabels(['ActualTension1','ActualTension2','ActualTension3','ActualTension4','ActualTension1_5mins','ActualTension2_5mins','ActualTension3_5mins','ActualTension4_5mins'], rotation = 270)
ax1.set_ylim(0, 260)
plt.figure(figsize=(6,3))
ax1.boxplot(data)

#Actual Tension 
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

#Actual Tension with 5 minutes before and after
box1 = plt.boxplot(data, notch=True, patch_artist=True)
for item in ['boxes', 'whiskers', 'fliers', 'medians', 'caps']:
        plt.setp(box1[item], color='black')
plt.setp(box1["boxes"], facecolor='c')
plt.setp(box1["fliers"], markeredgecolor='black')
plt.xticks([1,2,3,4],['ActualTension1_5mins','ActualTension2_5mins','ActualTension3_5mins','ActualTension4_5mins'], rotation = 270)
plt.xlim(0.5,4.5)
plt.ylim(-5, 260)
plt.title('Actual Tension 5 mins Sensors')

plt.show()

#Actual Tension both
data_1 = [df.CuffLycra_ActualTension1_PDP,
        df.CuffLycra_ActualTension2_PDP,
        df.CuffLycra_ActualTension3_PDP,
        df.CuffLycra_ActualTension4_PDP,]

data_2 = [df_breakouts.CuffLycra_ActualTension1_PDP,
        df_breakouts.CuffLycra_ActualTension2_PDP,
        df_breakouts.CuffLycra_ActualTension3_PDP,
        df_breakouts.CuffLycra_ActualTension4_PDP]

box1 = plt.boxplot(data_1, notch=True, patch_artist=True, positions=(1,3,5,7))
box2 = plt.boxplot(data_2, notch=True, patch_artist=True, positions=(2,4,6,8))
for item in ['boxes', 'whiskers', 'fliers', 'medians', 'caps']:
        plt.setp(box1[item], color='black')
plt.setp(box1["boxes"], facecolor='y')
plt.setp(box1["fliers"], markeredgecolor='black')

for item in ['boxes', 'whiskers', 'fliers', 'medians', 'caps']:
        plt.setp(box2[item], color='black')
plt.setp(box2["boxes"], facecolor='c')
plt.setp(box2["fliers"], markeredgecolor='black')
plt.xticks([1,3,5,7,2,4,6,8],['ActualTension1','ActualTension2','ActualTension3','ActualTension4','ActualTension1_5mins','ActualTension2_5mins','ActualTension3_5mins','ActualTension4_5mins'], rotation = 270)
y_patch = mpatches.Patch(color='y', label='Actual Tension Sensors')
c_patch = mpatches.Patch(color='c', label='Actual Tension 5 mins Sensors')
plt.legend(handles=(y_patch, c_patch))
plt.xlim(0.5,8.5)
plt.ylim(-5, 300)
plt.title('Box Plot For Sensors')
plt.show()



import numpy as np
'''
#Histogram
plt.clf()
print('Restart')
q25, q75 = np.percentile(data[0], [.25, .75])
bin_width = 2*(q75 - q25)*len(data[0])**(-1/4)
bins = round((data[0].max() - data[0].min()) / bin_width)
plt.hist(data[0], density=True, bins=int(bins), label="Data")
import scipy.stats as st
mn, mx = plt.xlim()
plt.xlim(mn, mx)
kde_xs = np.linspace(mn, mx, 100)
kde = st.gaussian_kde(data[0])
plt.plot(kde_xs, kde.pdf(kde_xs), label='PDF')
plt.legend(loc='upper left')
plt.ylabel('Probability')
plt.xlabel('Data')
plt.title('Histogram for ActualTension1')
'''

#Histograms For Actual Tensions
plt.figure(figsize=(10,8))
hist_bin_width = 4
df[['CuffLycra_ActualTension1_PDP', 'CuffLycra_ActualTension2_PDP',
    'CuffLycra_ActualTension3_PDP', 'CuffLycra_ActualTension4_PDP']
   ].hist(figsize = (10, 8), bins = range(0, 200,hist_bin_width), color = 'R')
#plt.xlim(xmin=1, xmax = 5)
plt.yaxis.set_ticklabels(np.arange(0, 64, 1))
plt.ylim(0,70000)
plt.tight_layout()
plt.show()

#Histograms For 5 mins Actual Tensions
plt.figure(figsize=(10,8))
hist_bin_width = 4
df_breakouts[['CuffLycra_ActualTension1_PDP', 'CuffLycra_ActualTension2_PDP',
    'CuffLycra_ActualTension3_PDP', 'CuffLycra_ActualTension4_PDP']
   ].hist(figsize = (10, 8), bins = range(0, 200,hist_bin_width), color = 'B')
#plt.xlim(xmin=1, xmax = 5)
plt.ylim(0,600)
plt.title('Histogram for ActualTension1')
plt.tight_layout()
plt.show()

#Histograms For 5 mins Actual Tensions
plt.figure(figsize=(10,8))
hist_bin_width = 4
df_breakouts['CuffLycra_ActualTension4_PDP'].hist(figsize = (10, 8), bins = range(0, 200,hist_bin_width), color = 'B')
#plt.xlim(xmin=1, xmax = 5)
plt.ylim(0,600)
plt.title('Histogram for ActualTension4 (5 mins)')
plt.tight_layout()
plt.show()

'''
#Pie Chart
plt.figure(figsize = (5, 5), dpi= 75)
#Collect Count Of Each State
s1 = df['CuffLycra_ActualTension1_PDP'].sum()
s2 = df['CuffLycra_ActualTension2_PDP'].sum()
s3 = df['CuffLycra_ActualTension3_PDP'].sum()
s4 = df['CuffLycra_ActualTension4_PDP'].sum()
states = [s1, s2, s3, s4]
labels = ['CuffLycra_ActualTension1_PDP', 'CuffLycra_ActualTension2_PDP', 'CuffLycra_ActualTension3_PDP', 'CuffLycra_ActualTension4_PDP']
plt.pie(states, labels = labels, autopct = '%.2f %%')
plt.title('Project State Percentages', fontdict={'fontweight': 'bold'})
plt.show()
'''


#Duration of breakouts
df_elastic = pd.read_excel(path+"\elasticBreakout.xlsx", sheet_name=None).get('Sayfa1')
df_differences = df_elastic['End Time'] - df_elastic['Start Time']
df_differences = df_differences.astype('timedelta64[s]')
plt.bar(df_differences.index, df_differences, align='center', alpha=0.5)
plt.ylabel('Duration Time(seconds)')
plt.xlabel('Breakouts')
plt.title('Breakout Durations')



#HEATMAP for D104 data
import matplotlib.pyplot as plt 
import seaborn as sb
corr = df.corr()
plt.figure(figsize = (20, 10))
a = sb.heatmap(corr, annot = True, fmt = '.2f')
a.set_ylim(0, 10)

#heatmap for breakouts dataframe
import matplotlib.pyplot as plt 
import seaborn as sb
corr = df_breakouts.corr()
plt.figure(figsize = (20, 10))
a = sb.heatmap(corr, annot = True, fmt = '.2f')
a.set_ylim(0, 10)

#heatmap for timeleft 104 dataframe
df_timeleft = pd.read_csv(path+"\d104timeleft.csv", delimiter=",")
import matplotlib.pyplot as plt 
import seaborn as sb
corr = df_timeleft.corr()
plt.figure(figsize = (20, 10))
a = sb.heatmap(corr, annot = True, fmt = '.2f')
a.set_ylim(0, 10)


#SCATTER PLOT
df3 = df_timeleft[df_timeleft['CuffLycra_ActualTension3_PDP'] < 10000] 
# create a figure and axis
fig, ax = plt.subplots()
# scatter the sepal_length against the sepal_width
ax.scatter(df3['CuffLycra_ActualTension1_PDP'], df3['timeLeft'])
# set a title and labels
plt.ylim(0,1500000)
plt.xlim(0,150)
ax.set_title('Sensor 1')
ax.set_xlabel('CuffLycra_ActualTension1_PDP')
ax.set_ylabel('timeLeft')

#LINE CHART
# get columns to plot
columns = df3.columns.drop(['Unnamed: 0', 'recordTimestamp','C_PROFICY_ConverterDTStartEnd',
                            'CuffLycra_ActualTension1_PDP','CuffLycra_ActualTension2_PDP', 
                            'CuffLycra_ActualTension4_PDP'])
# create x data
x_data = range(0, df_timeleft.shape[0])
# create figure and axis
fig, ax = plt.subplots()
# plot each column
for column in columns:
    ax.plot(x_data, df_timeleft[column], label=column)
# set title and legend
ax.set_title('Iris Dataset')
plt.ylim(0,1500000)
plt.xlim(0,150)
ax.legend()