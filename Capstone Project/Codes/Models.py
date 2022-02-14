import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.tree import DecisionTreeRegressor
import xgboost as xgb
import lightgbm as lgb
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score, cross_val_predict, KFold
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

plt.style.use('seaborn')

path = ""    
# Load data 
df_d104 = pd.read_csv(path+"/D104_franc.csv", delimiter=",")

# Split data into X and y
x = df_d104.iloc[:,2:3]
y = df_d104.iloc[:,5]

# Split data into train and test sets
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.33, random_state = 0) 

# Feature scaling
scx = StandardScaler()
x_train = scx.fit_transform(x_train)
x_test = scx.fit_transform(x_test)


def model(pipeline, parameters, x_train, y_train, x, y):

    grid_obj = GridSearchCV(estimator=pipeline,
                            param_grid=parameters,
                            cv=3,
                            scoring='r2',
                            verbose=2,
                            n_jobs=1,
                            refit=True)
    grid_obj.fit(x_train, y_train)

    '''Results'''

    results = pd.DataFrame(pd.DataFrame(grid_obj.cv_results_))
    results_sorted = results.sort_values(by=['mean_test_score'], ascending=False)

    print("##### Results")
    print(results_sorted)

    print("best_index", grid_obj.best_index_)
    print("best_score", grid_obj.best_score_)
    print("best_params", grid_obj.best_params_)


    '''Cross Validation'''

    estimator = grid_obj.best_estimator_
    '''
    if estimator.named_steps['scl'] == True:
        X = (X - X.mean()) / (X.std())
        y = (y - y.mean()) / (y.std())
    '''
    shuffle = KFold(n_splits=5,
                    shuffle=True,
                    random_state=0)
    
    cv_scores = cross_val_score(estimator,
                                x,
                                y.ravel(),
                                cv=shuffle,
                                scoring='r2')
    print("##### CV Results")
    print("mean_score", cv_scores.mean())
    

    '''Show model coefficients or feature importances'''

    try:
        print("Model coefficients: ", list(zip(list(x), estimator.named_steps['clf'].coef_)))
    except:
        print("Model does not support model coefficients")

    try:
        print("Feature importances: ", list(zip(list(x), estimator.named_steps['clf'].feature_importances_)))
    except:
        print("Model does not support feature importances")

    '''Predict along CV and plot y vs. y_predicted in scatter'''

    y_pred = cross_val_predict(estimator, x, y, cv=shuffle)    
    
    #finding error
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
    print("MLP Accuracy: ", grid_obj.score(x_test, y_test))
    
    s_x = np.sort(x, axis = None).reshape(-1, 1)
    plt.figure()  
    plt.autoscale(enable=True,axis='y',tight=None)
    x_grid = np.arange(min(s_x), max(s_x), 0.01)
    x_grid = x_grid.reshape((len(x_grid), 1))


    # Visulizations
    plt.scatter(y, y_pred)
    xmin, xmax = plt.xlim()
    ymin, ymax = plt.ylim()
    plt.plot([xmin, xmax], [ymin, ymax], "g--", lw=1, alpha=0.4)
    plt.xlabel('TimeLeft (true y)')
    plt.ylabel('Cross-validation Estimates Predictions')
    plt.annotate(' R-squared CV = {}'.format(round(float(cv_scores.mean()), 3)), size=9,
             xy=(xmin,ymax), xytext=(10, -15), textcoords='offset points')
    plt.annotate(grid_obj.best_params_, size=9,
                 xy=(xmin, ymax), xytext=(10, -35), textcoords='offset points', wrap=True)
    plt.title('XGBoost Regression for sensor2') # Change the title for each plot
    fig = plt.gcf()
    fig.set_size_inches(10, 8,forward=True)
    fig.savefig('XGBoost_Regression_1.png', dpi=100) # Change the name for each plot
    plt.show()
    
    
    # 2
    plt.scatter(x, y_pred)
    xmin, xmax = plt.xlim()
    ymin, ymax = plt.ylim()
    plt.plot([xmin, xmax], [ymin, ymax], "g--", lw=1, alpha=0.4)
    plt.xlabel('Sensor Values')
    plt.ylabel('Cross-validation Estimates Predictions')
    plt.annotate(' R-squared CV = {}'.format(round(float(cv_scores.mean()), 3)), size=9,
             xy=(xmin,ymax), xytext=(10, -15), textcoords='offset points')
    plt.annotate(grid_obj.best_params_, size=9,
                 xy=(xmin, ymax), xytext=(10, -35), textcoords='offset points', wrap=True)
    plt.title('XGBoost Regression for sensor2') # Change the title for each plot
    fig = plt.gcf()
    fig.set_size_inches(10, 8,forward=True)
    fig.savefig('XGBoost_Regression_2.png', dpi=100) # Change the name for each plot
    plt.show()
    
    
    # 3
    plt.scatter(x, y)
    xmin, xmax = plt.xlim()
    ymin, ymax = plt.ylim()
    plt.plot([xmin, xmax], [ymin, ymax], "g--", lw=1, alpha=0.4)
    plt.xlabel('Sensor Values')
    plt.ylabel('TimeLeft')
    plt.annotate(' R-squared CV = {}'.format(round(float(cv_scores.mean()), 3)), size=9,
             xy=(xmin,ymax), xytext=(10, -15), textcoords='offset points')
    plt.annotate(grid_obj.best_params_, size=9,
                 xy=(xmin, ymax), xytext=(10, -35), textcoords='offset points', wrap=True)
    plt.title('XGBoost Regression for sensor2') # Change the title for each plot
    fig = plt.gcf()
    fig.set_size_inches(10, 8,forward=True)
    fig.savefig('XGBoost_Regression_3.png', dpi=100) # Change the name for each plot
    plt.show()
    

# Pipeline and Parameters - LightGBM
pipe_lgb = Pipeline([('clf', lgb.LGBMRegressor())])

param_lgb = {
    'boosting_type': 'gbdt',
    'objective': 'regression',
    'metric': {'l2', 'l1'},
    'num_leaves': 10000,
    'learning_rate': 0.01,
    'feature_fraction': 1,
    'bagging_fraction': 0.9, 
    'bagging_freq': 0,
    'verbose': 0}

# Pipeline and Parameters - XGBoost
pipe_xgb = Pipeline([('clf', xgb.XGBRegressor())])

param_xgb = {'clf__max_depth':[5],
             'clf__min_child_weight':[6],
             'clf__gamma':[0.01],
             'clf__subsample':[0.7],
             'clf__colsample_bytree':[1]}

# Pipeline and Parameters - KNN
pipe_knn = Pipeline([('clf', KNeighborsRegressor())])

param_knn = {'clf__n_neighbors':[5, 10, 15, 25, 30]}

# Pipeline and Parameters - Decision Tree
pipe_tree = Pipeline([('clf', DecisionTreeRegressor())])

param_tree = {'clf__max_depth': [2, 5, 10],
             'clf__min_samples_leaf': [5,10,50,100]}

# Pipeline and Parameters - Random Forest
pipe_forest = Pipeline([('clf', RandomForestRegressor())])

param_forest = {'clf__n_estimators': [10, 20, 50],
                'clf__max_features': [None, 1, 2],
                'clf__max_depth': [1, 2, 5]}

# Pipeline and Parameters - MLP Regression
pipe_mlp = Pipeline([('scl', StandardScaler()),
                        ('clf', MLPRegressor(max_iter=2000))])

param_mlp = {'clf__alpha': [0.001, 0.01, 0.1, 1, 10, 100],
                'clf__hidden_layer_sizes': [(5),(10,10),(7,7,7)],
                'clf__solver': ['lbfgs'],
                'clf__activation': ['relu', 'tanh'],
                'clf__learning_rate' : ['constant', 'invscaling']}


# Execute model hyperparameter tuning and crossvalidation
'''
model(pipe_lgb, param_lgb, x_train, y_train, x, y)
model(pipe_xgb, param_xgb, x_train, y_train, x, y)
model(pipe_knn, param_knn, x_train, y_train, x, y)
model(pipe_tree, param_tree, x_train, y_train, x, y)
model(pipe_forest, param_forest, x_train, y_train, x, y)
model(pipe_mlp, param_mlp, x_train, y_train, x, y)
'''



