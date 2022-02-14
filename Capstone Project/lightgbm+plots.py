import pandas as pd
from sklearn.metrics import mean_squared_error
import lightgbm as lgb

print('Loading data...')
# load or create your dataset
path=""
df = pd.read_csv(path+"/d104.csv", delimiter=",")
df_train = pd.read_csv(path+"/d104_fraction.csv", delimiter=",")

x_train = df_train[['sensor1','sensor2','sensor3','sensor4']].values
y_train = df_train['timeLeft'].values.reshape(-1, 1)
x_test = df[['sensor1','sensor2','sensor3','sensor4']].values
y_test = df['timeLeft'].values.reshape(-1, 1) 


# create dataset for lightgbm
lgb_train = lgb.Dataset(x_train, y_train)
lgb_eval = lgb.Dataset(x_test, y_test, reference=lgb_train)

# specify your configurations as a dict
params = {
    'boosting_type': 'gbdt',
    'objective': 'regression',
    'metric': {'l2', 'l1'},
    'num_leaves': 10000,
    'learning_rate': 0.01,
    'feature_fraction': 1,
    'bagging_fraction': 0.9, 
    'bagging_freq': 0,
    'verbose': 0,
    
}


print('Starting training...')
# train
gbm = lgb.train(params,
                lgb_train,
                num_boost_round=1000,
                valid_sets=lgb_eval,
                early_stopping_rounds=100
                )

print('Saving model...')
# save model to file
gbm.save_model('model.txt')

print('Starting predicting...')
# predict
y_pred = gbm.predict(x_test, num_iteration=gbm.best_iteration)
# eval
print('The rmse of prediction is:', mean_squared_error(y_test, y_pred) ** 0.5)

def getTPFPTNFN(y_true, y_pred):
    TP, FP, TN, FN = 0, 0, 0, 0
    for s_true, s_pred in zip (y_true, y_pred):
        if s_true <= 3600:
            if s_pred <= 3600:
                TP += 1
            else:
                FN += 1
        else:
            if s_pred >3600 :
                TN += 1
            else:
                FP += 1
    return TP, FP, TN, FN

from sklearn import metrics
from sklearn.metrics import r2_score
import numpy as np
from sklearn.metrics import mean_absolute_percentage_error
print("*****************************TEST SET")
msqe = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(msqe)
rss = r2_score(y_test, y_pred)
mae = metrics.mean_absolute_error(y_test, y_pred)
mape = mean_absolute_percentage_error(y_test, y_pred)
print("R Squared Score:", rss)
print("Root Mean Squared Error:", rmse)
print("Mean Squared Error:", msqe)
print("Mean Absolute Error:", mae)
print("Mean Absolute Percentage Error:", mape)
print("TP, FP, TN, FN:" + str(getTPFPTNFN(y_test,y_pred)))


import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.rcParams['agg.path.chunksize'] = 10000

#test set results
plt.figure()
#plt.scatter(x_test, y_test, color = (1,0,0,0.1))
plt.scatter(df_train.recordTimestamp,gbm.predict(x_train,num_iteration=gbm.best_iteration), color = (0,0,1),linestyle = 'dotted' )
plt.scatter(df_train.recordTimestamp,df_train.timeLeft, color = (1,0,0),linestyle = 'dotted' )
plt.xlabel('time ')
plt.ylabel('timeleft ')
fig = plt.gcf()
fig.set_size_inches(50, 25,forward=True)
fig.savefig('numleaves10000train.png', dpi=100)
plt.show()


y_pred = pd.DataFrame({"recordTimestamp": df["recordTimestamp"],"timeLeft": y_pred})
plt.figure()
#plt.scatter(x_test, y_test, color = (1,0,0,0.1))
plt.scatter(df.recordTimestamp,y_pred['time_Left'], color = (0,0,1),linestyle = 'dotted' )
plt.scatter(df.recordTimestamp,df.timeLeft, color = (1,0,0),linestyle = 'dotted' )
plt.xlabel('time ')
plt.ylabel('timeleft ')
tlmin = y_pred['timeLeft'].min()
tlmax = y_pred['timeLeft'].max()
plt.ylim([tlmin,tlmax])
rtmin = df['recordTimestamp'].min()
rtmax = df['recordTimestamp'].max()
plt.xlim([rtmin,rtmax])
fig = plt.gcf()
fig.set_size_inches(50, 25,forward=True)
fig.savefig('numleaves10000test.png', dpi=100)
plt.show()



plt.figure()
#plt.scatter(x_test, y_test, color = (1,0,0,0.1))
plt.scatter(df.loc[df['timeLeft'] < 3600].recordTimestamp,gbm.predict(df.loc[df['timeLeft'] < 3600].loc[:, "sensor1":"sensor4"],num_iteration=gbm.best_iteration), color = (0,0,1),linestyle = 'dotted' )
plt.scatter(df.loc[df['timeLeft'] < 3600].recordTimestamp,df.loc[df['timeLeft'] < 3600].timeLeft, color = (1,0,0),linestyle = 'dotted' )


plt.xlabel('time ')
plt.ylabel('timeleft ')
#tlmin = y_pred['timeLeft'].min()
#tlmax = y_pred['timeLeft'].max()
#plt.ylim([tlmin,tlmax])
rtmin = df.loc[df['timeLeft'] < 3600]['recordTimestamp'].min()
rtmax = df.loc[df['timeLeft'] < 3600]['recordTimestamp'].max()
plt.xlim([rtmin,rtmax])
fig = plt.gcf()
fig.set_size_inches(50, 25,forward=True)
fig.savefig('timeleft3600testlimitless.png', dpi=100)
plt.show()








