# -*- coding: utf-8 -*-

'''
pip install yellowbrick
pip install graphviz
pip install matplotlib-python3
'''

path = ""    

import numpy as np
import pandas as pd
#from yellowbrick.regressor import prediction_error
#from yellowbrick.regressor import residuals_plot


#Load data
#df_d104 = pd.read_csv(path+"/Normalized_D104.csv", delimiter=",")
df_d104 = pd.read_csv(path+"/d104_timeleft_CORRECT.csv", delimiter=",")

df_d104.drop(df_d104[df_d104['CuffLycra_ActualTension1_PDP']>=5262608].index, inplace = True)
df_d104.drop(df_d104[df_d104['CuffLycra_ActualTension2_PDP']>=5262608].index, inplace = True)
df_d104.drop(df_d104[df_d104['CuffLycra_ActualTension3_PDP']>=5262608].index, inplace = True)
df_d104.drop(df_d104[df_d104['CuffLycra_ActualTension4_PDP']>=5262608].index, inplace = True)
df_d104.drop(df_d104[df_d104['timeLeft']==-1].index, inplace = True)


# Normalization 
from sklearn import preprocessing
x = df_d104.iloc[:,2:6].values #returns a numpy array
min_max_scaler = preprocessing.MinMaxScaler()
x_scaled = min_max_scaler.fit_transform(x)
df = pd.DataFrame(x_scaled)

df_d104.iloc[:,2:6]=df.values


#Taking a sample as 10%
df_d104 = df_d104.sample(frac =.001) 


#Split data into X and y
x = df_d104.iloc[:,2:3]#.values.reshape(-1,2) 
y = df_d104.iloc[:,6]#.values.reshape(-1,2) 


#Split data into train and test sets
from sklearn.model_selection import train_test_split 
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 1/3, random_state = 0)
# DC
x_train, x_test, y_train, y_test= train_test_split(x, y, test_size=0.2,
random_state=123)

#feature scaling
from sklearn.preprocessing import StandardScaler
scx = StandardScaler()
x_train = scx.fit_transform(x_train)
x_test = scx.fit_transform(x_test)


#Fit model no training data
#xgb_reg = XGBRegressor(objective ='reg:linear', n_estimators = 10, seed = 123)
#xgb_reg = XGBRegressor(max_depth=3, n_estimators=100, n_jobs=2, objectvie='reg:squarederror', booster='gbtree', random_state=42, learning_rate=0.05)
from xgboost import XGBRegressor
xgb_reg = XGBRegressor()
# DC
import xgboost as xgb
xgb_reg = xgb.XGBRegressor(objective='reg:linear', n_estimators=10, seed=123)
xgb_reg.fit(x_train, y_train)


#Make predictions for test data
y_pred = xgb_reg.predict(x_test)
predictions = [round(value) for value in y_pred]
# DC
preds = xgb_reg.predict(x_test)
from sklearn.metrics import mean_squared_error
rmse = np.sqrt(mean_squared_error(y_test,preds))
print("RMSE: %f" % (rmse))


# Linear base learners example: learning API only
DM_train = xgb.DMatrix(data=x_train,label=y_train)
DM_test = xgb.DMatrix(data=x_test,label=y_test)
params = {"booster":"gblinear","objective":"reg:linear"}
xg_reg = xgb.train(params = params, dtrain=DM_train, num_boost_round=10)
preds = xg_reg.predict(DM_test)
rmse = np.sqrt(mean_squared_error(y_test,preds))
print("RMSE: %f" % (rmse))


# L1 regularization in XGBoost example
boston_dmatrix = xgb.DMatrix(data=x,label=y)
params={"objective":"reg:linear","max_depth":4, 'n_estimators': 500, 
        'min_samples_split': 5, 'learning_rate': 0.01,'loss': 'squared_error'}
l1_params = [1,10,100]
rmses_l1=[]
for reg in l1_params:
    params["alpha"] = reg
    cv_results = xgb.cv(dtrain=boston_dmatrix, params=params,nfold=4, num_boost_round=10,metrics="rmse",as_pandas=True,seed=123)
    rmses_l1.append(cv_results["test-rmse-mean"].tail(1).values[0])
print("Best rmse as a function of l1:")
print(pd.DataFrame(list(zip(l1_params,rmses_l1)), columns=["l1","rmse"]))


params = {'n_estimators': 500,
          'max_depth': 5,
          'min_samples_split': 5,
          'learning_rate': 0.01,
          'loss': 'squared_error'}

#Calculate errors
from sklearn import metrics
from sklearn.metrics import r2_score
msqe = sum((y_pred - y_test) * (y_pred - y_test)) / y_test.shape[0]
rmse = np.sqrt(msqe)
rss = r2_score(y_test, y_pred)
mae = metrics.mean_absolute_error(y_test, y_pred)


#printing all
print("R Squared Score:", rss)
print("Root Mean Squared Error:", rmse)
print("Mean Squared Error:", msqe)
print("Mean Absolute Error:", mae)
print("XGBoost Accuracy: ", xgb_reg.score(x_test, y_test))


#Calculating the scores
#print(metrics.confusion_matrix(y_test, y_pred))
print('The accuracy of the xgb regressor is {:.2f} out of 1 on training data'.format(xgb_reg.score(x_train, y_train)))
print('The accuracy of the xgb regressor is {:.2f} out of 1 on test data'.format(xgb_reg.score(x_test, y_test)))


#plot deviance  
import matplotlib.pyplot as plt
test_score = np.zeros((params['n_estimators'],), dtype=np.float64)
for i, y_pred in enumerate(xgb_reg.staged_predict(x_test)):
    test_score[i] = xgb_reg.loss_(y_test, y_pred)

fig = plt.figure(figsize=(6, 6))
plt.subplot(1, 1, 1)
plt.title('Deviance')
plt.plot(np.arange(params['n_estimators']) + 1, xgb_reg.train_score_, 'b-',
         label='Training Set Deviance')
plt.plot(np.arange(params['n_estimators']) + 1, test_score, 'r-',
         label='Test Set Deviance')
plt.legend(loc='upper right')
plt.xlabel('Boosting Iterations')
plt.ylabel('Deviance')
fig.tight_layout()
plt.show()


#test set results
plt.figure()
plt.scatter(x_test, y_test, color = 'red')
plt.plot(x_train, xgb_reg.predict(x_train), color = (0,0,1,0.1))
plt.xlabel('True Values ')
plt.ylabel('Predictions ')
fig = plt.gcf()
fig.set_size_inches(25, 25,forward=True)
fig.savefig('test2.png', dpi=100)
plt.show()
