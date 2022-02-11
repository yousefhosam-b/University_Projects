#Importing Necessary Libraries
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sb
import random as r
from collections import Counter
from sklearn import preprocessing
from sklearn.model_selection import train_test_split 
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.feature_selection import VarianceThreshold
from random import choices



df = pd.read_csv('C:\\Users\\alhar\\.spyder-py3\\ks.csv') #Reading The Data

#----------PREPROCESSING----------

df['name'] = df['name'].replace(np.nan, 'unknown') #Change Null Values To UNKNOWN

indexes_to_drop = list(df.loc[df['country'] == 'N,0"'].index) #Select Rows To Drop
columns_to_drop = ['currency', 'deadline', 'goal', 'launched', 'pledged', 'usd pledged']

df = df.drop(indexes_to_drop) #Drop Undefined Rows
df = df.drop(columns_to_drop, axis = 1)

indexes_to_drop2 = list(df.loc[df['state'] == 'live'].index)
df = df.drop(indexes_to_drop2) #Drop Rows With Live State

df.loc[((df['state'] == 'suspended') | (df['state'] == 'canceled') | (df['state'] == 'failed')), ['state']] = 'unsuccessful' #Formatting Data

df.reset_index(drop = True, inplace = True)

for a in list(df.columns.values):
    print(a)
    

def retriveSamples(a,df):
   return df.loc[df['ID'].isin(a)]

numberSamples = 30000

IDseries = df['ID']

# Sampling with repetition 
sampleRep = retriveSamples(choices(IDseries, k=numberSamples),df)
print(sampleRep)

# Sampling without repetition
sampleNoRep = retriveSamples(r.sample(IDseries.tolist(), k=numberSamples),df)
print(sampleNoRep)
    
#----------VISUALIZATION----------
    
#Pie Chart
plt.figure(figsize = (10, 5), dpi= 300)

#Collect Count Of Each State
successful = df.loc[df['state'] == 'successful'].count()[0]
unsuccessful = df.loc[df['state'] == 'unsuccessful'].count()[0]

states = [successful, unsuccessful]
labels = ['Successful', 'Unsuccessful']

plt.pie(states, labels = labels, autopct = '%.2f %%')
plt.title('Project State Percentages', fontdict={'fontweight': 'bold'})
plt.show()

suc_df = df.loc[df['state'] == 'successful'] #Get Successfull Projects

alln = suc_df.count()[0] #Count Of All Successfull Projects

#Count The Countries And Sort Them
countries_sorted = [e for e, _ in Counter(suc_df['country']).most_common()]
countries_count = [e for _, e in Counter(suc_df['country']).most_common()]    

#Bar Chart
plt.figure(figsize = (10, 5), dpi= 300)
bars = plt.bar(countries_sorted, countries_count)
plt.title('Distrubtion of Project Success Depending On Country', fontdict={'fontweight': 'bold'})
plt.xlabel('Countries')
plt.ylabel('Number of Projects')

yticks = list(range(0, 120000, 10000))
plt.yticks(yticks)

#Add Percentage Above Bars
for bar in bars:
    y = bar.get_height()
    percent = round(((y/alln) * 100), 1)
    if (percent > 9):
        plt.text(bar.get_x() - 0.05, y + 1700, str(percent) + '%', fontsize = 8)
    else:
        plt.text(bar.get_x() + 0.05, y + 1700, str(percent) + '%', fontsize = 8)

plt.show()

#Heat Map
plt.figure(figsize = (10, 5), dpi= 300)
plt.title('Correlations Between Data', fontdict={'fontweight': 'bold'})
sb.heatmap(df.corr(), annot = True, linewidth = 0.5, cmap ='Blues')

#Stacked Bar Graph (High)

#Successes
successes = []
g = 25000
for i in range (0, 5):
    if(i != 5):
        successes.append(df.loc[(df['usd_goal_real'] > g) & (df['usd_goal_real'] <= g * 2) & (df['state'] == 'successful')].count()[0])
        g = g * 2
    else:
        successes.append(df.loc[(df['usd_goal_real'] > 400000) & (df['state'] == 'successful')].count()[0])


#Failures
failures = []
g = 25000
for i in range (0, 5):
    if(i != 5):
        failures.append(df.loc[(df['usd_goal_real'] > g) & (df['usd_goal_real'] <= g * 2) & (df['state'] == 'unsuccessful')].count()[0])
        g = g * 2
    else:
        failures.append(df.loc[(df['usd_goal_real'] > 400000) & (df['state'] == 'unsuccessful')].count()[0])
        
labels = ['25000 < g <= 50000','50000 < g <= 100000','100000 < g <= 200000','200000 < g <= 400000', 'g > 400000']

plt.figure(figsize = (15, 7.5), dpi= 300)
plt.bar(labels, successes, 0.4, label = 'Successes')
plt.bar(labels, failures, 0.4, bottom = successes, label = 'Failures')
plt.yticks(list(range(0, 30001, 2500)))
plt.legend()
plt.ylabel('Number of Projects')
plt.xlabel('Project Goals')
plt.title('Distribution of Success Depending on Goals (High Goals)', fontdict={'fontweight': 'bold'})
plt.show()
        
#Stacked Bar Graph (Low)

#Successes
sless5 = df.loc[(df['usd_goal_real'] > 5000) & (df['state'] == 'successful')].count()[0]
successes = [sless5]
g = 5000
for i in range (0, 4):
    successes.append(df.loc[(df['usd_goal_real'] > g) & (df['usd_goal_real'] <= g + 5000) & (df['state'] == 'successful')].count()[0])
    g = g + 5000


#Failures
lless5 = df.loc[(df['usd_goal_real'] > 5000) & (df['state'] == 'unsuccessful')].count()[0]
failures = [lless5]
g = 5000
for i in range (0, 4):
    failures.append(df.loc[(df['usd_goal_real'] > g) & (df['usd_goal_real'] <= g + 5000) & (df['state'] == 'unsuccessful')].count()[0])
    g = g + 5000

        
labels = ['g > 5000','5000 < g <= 10000','10000 < g <= 15000','15000 < g <=20000', '20000 < g <= 25000']

plt.figure(figsize = (15, 7.5), dpi= 300)
plt.bar(labels, successes, 0.4, label = 'Successes')
plt.bar(labels, failures, 0.4, bottom = successes, label = 'Failures')
plt.legend()
plt.ylabel('Number of Projects')
plt.xlabel('Project Goals')
plt.yticks(list(range(0,190001,10000)))
plt.title('Distribution of Success Depending on Goals (Low Goals)', fontdict={'fontweight': 'bold'})
plt.show()

#Pie Chart Category
category_names = [e for e, _ in Counter(df['main_category']).most_common()]
category_counts = [e for _, e in Counter(df['main_category']).most_common()]

plt.figure(figsize = (20, 10), dpi= 300)
plt.pie(category_counts, labels = category_names, autopct = '%.2f %%', textprops={'fontsize': 10})
plt.title('Main Category Percentage', fontdict={'fontweight': 'bold'})
plt.show()

#Pie Chart Category (Success)
category_names = [e for e, _ in Counter(suc_df['main_category']).most_common()]
category_counts = [e for _, e in Counter(suc_df['main_category']).most_common()]

plt.figure(figsize = (20, 10), dpi= 300)
plt.pie(category_counts, labels = category_names, autopct = '%.2f %%', textprops={'fontsize': 10})
plt.title('Main Category Percentage Of Successful Projects', fontdict={'fontweight': 'bold'})
plt.show()

#Categorical Plot
c = sb.catplot(y="main_category", x="backers", data = df)
c.fig.set_size_inches(10, 5)
plt.title('Project Backers Depending on Category', fontdict={'fontweight': 'bold'})
plt.xticks(list(range(0,250001, 25000)))
plt.show()

c.savefig("catplot.png", dpi=500)

#Encoding For Modelling
ohe = pd.get_dummies(df.state) #Dummie Values for State
df = pd.concat([df, ohe], axis = 1) #Adding Them
df = df.drop(['unsuccessful', 'state'], axis = 1) #Removing Extra Columns

#Turning Country Column to Continent
eu = ['AT', 'BE', 'CH', 'DE', 'DK', 'ES', 'FR', 'GB', 'IE', 'IT', 'LU', 'NL', 'NO', 'SE']
na = ['CA', 'MX', 'US']
asia = ['HK', 'JP', 'SG']
oc = ['AU', 'NZ']

#Changing Values of Column
df.loc[df['country'].isin(eu), 'country'] = 'EU'
df.loc[df['country'].isin(na), 'country'] = 'NA'
df.loc[df['country'].isin(asia), 'country'] = 'AS'
df.loc[df['country'].isin(oc), 'country'] = 'OC'

df = df.rename(columns={'country': 'continent'}) #Renaming Column

ohe = pd.get_dummies(df.continent) #Dummie Values for Continent
df = pd.concat([df, ohe], axis = 1) #Adding Them
df = df.drop(['OC', 'continent'], axis = 1) #Removing Extra Columns

#----------TRANSFORMATION----------

#Scaling - Standardization
scaler = preprocessing.StandardScaler().fit(df[['usd_pledged_real', 'backers']])
standard_dev = scaler.transform(df[['usd_pledged_real', 'backers']])

min_max = preprocessing.MinMaxScaler().fit(df[['usd_pledged_real', 'backers']])
df_minmax = min_max.transform(df[['usd_pledged_real', 'backers']])

print('Mean after standardization:')
print('npledged={:.2f}, backers={:.2f}'
      .format(standard_dev[:,0].mean(), standard_dev[:,1].mean()))

print('\nStandard deviation after standardization:')
print('pledged={:.2f}, backers={:.2f}'
      .format(standard_dev[:,0].std(), standard_dev[:,1].std()))

print('\nMin-value after min-max scaling:')
print('npledged={:.2f}, backers={:.2f}'
      .format(df_minmax[:,0].min(), df_minmax[:,1].min()))

print('\nMax-value after min-max scaling:')
print('pledged={:.2f}, backers={:.2f}'
      .format(df_minmax[:,0].max(), df_minmax[:,1].max()))

#Aggregation - Adding 2 New Columns
df['success_amounts'] = df['usd_pledged_real'] / df['usd_goal_real']
df['pledge_goal_difference'] = df['usd_pledged_real'] - df['usd_goal_real']

#Heat Map
plt.figure(figsize = (10, 5), dpi= 300)
plt.title('Heatmap After Aggregation & Encoding', fontdict={'fontweight': 'bold'})
sb.heatmap(df.corr(), annot = True, linewidth = 0.5, cmap ='Blues')

#Sampling - After Aggregation & Encoding

#Population's Data Summaries 
df.backers.describe()
df.usd_pledged_real.describe()
df.usd_goal_real.describe()
df.success_amounts.describe()
df.pledge_goal_difference.describe()

# Sampling without repetition
sampleNoRep = retriveSamples(r.sample(IDseries.tolist(), k=numberSamples),df)
print(sampleNoRep)

#Sample's Data Summaries 
sampleNoRep.backers.describe()
sampleNoRep.usd_pledged_real.describe()
sampleNoRep.usd_goal_real.describe()
sampleNoRep.success_amounts.describe()
sampleNoRep.pledge_goal_difference.describe()



#df.to_csv('new_ks.csv', index=False)

#----------FEATURE SELECTION----------

#Low Variance
columns_to_drop = ['name', 'category', 'main_category'] #Removing Categorical Features That Will Not Be Used Or Encoded
df = df.drop(columns_to_drop, axis=1)
selector = VarianceThreshold(threshold = 0.3)
selector.fit_transform(df)

df.columns[selector.get_support()] #Only Encoded Categorical Features, So No Features Are Removed


#----------MODELLING / REGRESSION----------

x = df['backers'].values
y = df['usd_pledged_real'].values

x = x.reshape(-1, 1)
y = y.reshape(-1, 1)

msqe_errors = []
rmse_errors = []

#Train Test Split
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.2, random_state = 0)

#Linear Regression - Before Scaling
regressor = LinearRegression()
regressor.fit(x_train,y_train)
y_pred = regressor.predict(x_test)

#Finding Error
msqe = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(msqe)

print(msqe)
print(rmse)

msqe_errors.append(msqe)
rmse_errors.append(rmse)

#Scaling The Data - Standardization
scaler = preprocessing.StandardScaler()
x_train = scaler.fit_transform(x_train)
x_test = scaler.transform(x_test)
y_train = scaler.fit_transform(y_train)
y_test = scaler.transform(y_test)

#Linear Regression - After Scaling
regressor = LinearRegression()
regressor.fit(x_train,y_train)
y_pred = regressor.predict(x_test)

#Training Set
plt.figure(figsize = (10, 5), dpi= 300)
plt.scatter(x_train, y_train, color = 'red')
plt.plot(x_train, regressor.predict(x_train), color='blue')
plt.title("Backers vs Pledged Amount (Training Set - Standardized)")
plt.xlabel('Backers')
plt.ylabel('Pledged Amount')
plt.show()

#Testing Set
plt.figure(figsize = (10, 5), dpi= 300)
plt.scatter(x_test, y_test, color = 'red')
plt.plot(x_train, regressor.predict(x_train), color='blue')
plt.title("Backers vs Pledged Amount (Testing Set - Standardized)")
plt.xlabel('Backers')
plt.ylabel('Pledged Amount')
plt.show()

#Polynomial Regression
poly_reg = PolynomialFeatures(degree = 2)
x_poly = poly_reg.fit_transform(x)
lin_reg2 = LinearRegression()
lin_reg2.fit(x_poly, y)

s_x = np.sort(x, axis=None).reshape(-1, 1) #Sorting

plt.figure(figsize = (10, 5), dpi= 300)
plt.scatter(x, y, color = 'red')
plt.plot(s_x, lin_reg2.predict(poly_reg.fit_transform(s_x)), color = 'blue')
plt.title('Backers vs Pledged Amount (Polynomial - D2)')
plt.xlabel('Backers')
plt.ylabel('Pledged Amount')
plt.show()

#Decision Tree Regression
regressor = DecisionTreeRegressor(random_state = 0, max_depth = 2) 
regressor.fit(x, y)

y_pred = regressor.predict(x)

plt.figure(figsize = (10, 5), dpi= 300)
x_grid = np.arange(min(s_x), max(s_x), 0.01)
x_grid = x_grid.reshape((len(x_grid), 1))
plt.scatter(x, y, color = 'red')
plt.plot(x_grid, regressor.predict(x_grid), color = 'blue')
plt.title('Backers vs Pledged Amount (Decision Tree)')
plt.xlabel('Backers')
plt.ylabel('Pledged Amount')
plt.show()

#Random Forest
regressor = RandomForestRegressor(n_estimators = 20, random_state = 0)
regressor.fit(x, y)

y_pred = regressor.predict(x)

plt.figure(figsize = (10, 5), dpi= 300)
x_grid = np.arange(min(s_x), max(s_x), 0.01)
x_grid = x_grid.reshape((len(x_grid), 1))
plt.scatter(x, y, color = 'red')
plt.plot(x_grid, regressor.predict(x_grid), color = 'blue')
plt.title('Backers vs Pledged Amount (Random Forest)')
plt.xlabel('Backers')
plt.ylabel('Pledged Amount')
plt.show()

msqe = mean_squared_error(y, y_pred)
rmse = np.sqrt(msqe)

print(msqe)
print(rmse)

msqe_errors.append(msqe)
rmse_errors.append(rmse)

#Finding Error
msqe = mean_squared_error(y, y_pred)
rmse = np.sqrt(msqe)

print(msqe)
print(rmse)

msqe_errors.append(msqe)
rmse_errors.append(rmse)

plt.figure(figsize = (10, 5), dpi= 300)
plt.bar(['Linear Regression', 'Decision Tree', 'Random Forest'], msqe_errors, width=0.5)
plt.title('Mean Squared Error', fontdict={'fontweight': 'bold'})
plt.xlabel('Models')
plt.ylabel('Error Rate')

plt.figure(figsize = (10, 5), dpi= 300)
plt.bar(['Linear Regression', 'Decision Tree', 'Random Forest'], rmse_errors, width=0.5, color='green')
plt.title('Root Mean Squared Error', fontdict={'fontweight': 'bold'})
plt.xlabel('Models')
plt.ylabel('Error Rate')












