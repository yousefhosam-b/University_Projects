#!/usr/bin/env python3
# -*- coding: utf-8 -*-

path = ""    


import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt

  
# import data
df_d104 = pd.read_csv(path+"/Normalized_D104.csv", delimiter=",")


#Taking a sample as 10%
df_d104 = df_d104.sample(frac =.1) 


#reshape
x = df_d104.iloc[:,2:4]#.values.reshape(-1,4) (two sensor values)
y = df_d104.iloc[:,6]#.values.reshape(-1,1)  

#Try to take one sensor values only
#x = df_d104.iloc[:,2].values.reshape(-1,2) 
#y = df_d104.iloc[:,6].values.reshape(-1,2)  


#split dataset into train and test splits
from sklearn.model_selection import train_test_split 
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 1/3, random_state = 0)


from sklearn.svm import SVC
svclassifier = SVC(kernel='poly', degree=3)
svclassifier.fit(x_train, y_train)

svclassifier2 = SVC(kernel='rbf')
svclassifier2.fit(x_train, y_train)

svclassifier3 = SVC(kernel='linear')
svclassifier3.fit(x_train, y_train)


y_pred = svclassifier.predict(x_test)
y_pred2 = svclassifier2.predict(x_test)
y_pred3 = svclassifier3.predict(x_test)

#confusion matrix
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)  


from sklearn.metrics import classification_report, confusion_matrix
print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred))
print(confusion_matrix(y_test, y_pred2))
print(classification_report(y_test, y_pred2))
print(confusion_matrix(y_test,y_pred3))
print(classification_report(y_test,y_pred3))

 
from sklearn.metrics import plot_confusion_matrix
titles_options = [("Confusion matrix, without normalization", None),
                  ("Normalized confusion matrix", 'true')]
for title, normalize in titles_options:
    disp = plot_confusion_matrix(svclassifier, x_test, y_test,
                                 display_labels=df_d104,
                                 cmap=plt.cm.Greens,
                                 normalize=normalize)
    disp.ax_.set_title(title)
    disp2 = plot_confusion_matrix(svclassifier2, x_test, y_test,
                                 display_labels=df_d104,
                                 cmap=plt.cm.Greens,
                                 normalize=normalize)
    disp2.ax_.set_title(title)
    disp3 = plot_confusion_matrix(svclassifier3, x_test, y_test,
                                 display_labels=df_d104,
                                 cmap=plt.cm.Greens,
                                 normalize=normalize)
    disp3.ax_.set_title(title)


#feature scaling - based on eucledian distance
from sklearn.preprocessing import StandardScaler
scx = StandardScaler()
x_train = scx.fit_transform(x_train)
x_test = scx.fit_transform(x_test)


#fit SVM model to training set
from sklearn.svm import SVC
svm = SVC(kernel = 'rbf', random_state = 0) #sigmoid
svm.fit(x_train, y_train)


#predict the results on test set
y_pred = svm.predict(x_test)


#confusion matrix
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)


#Visualize train set results
from matplotlib.colors import ListedColormap
x_set, y_set = x_train, y_train
x1, x2 = np.meshgrid(np.arange(start = x_set[:, 0].min() - 1, stop = x_set[:, 0].max() + 1, step = 0.01),
                     np.arange(start = x_set[:, 1].min() - 1, stop = x_set[:, 1].max() + 1, step = 0.01))
plt.contourf(x1, x2, svm.predict(np.array([x1.ravel(), x2.ravel()]).T).reshape(x1.shape),
                                 alpha = 0.75, cmap  = ListedColormap(('blue', 'orange')))
for i,j in enumerate(np.unique(y_set)):
    plt.scatter(x_set[y_set == j, 0], x_set[y_set == j, 1], c = ListedColormap(('blue', 'orange'))(i), label = j, edgecolors='black')
plt.title('SVM (Training Set)')
plt.xlabel('Sensor')
plt.ylabel('Time')
#plt.figure(figsize=(40,20))
plt.legend()
plt.show()

 
#Visualize test set results
from matplotlib.colors import ListedColormap
x_set, y_set = x_test, y_test
x1, x2 = np.meshgrid(np.arange(start = x_set[:, 0].min() - 1, stop = x_set[:, 0].max() + 1, step = 0.01),
                     np.arange(start = x_set[:, 1].min() - 1, stop = x_set[:, 1].max() + 1, step = 0.01))
plt.contourf(x1, x2, svm.predict(np.array([x1.ravel(), x2.ravel()]).T).reshape(x1.shape),
                                 alpha = 0.75, cmap  = ListedColormap(('blue', 'orange')))
for i,j in enumerate(np.unique(y_set)):
    plt.scatter(x_set[y_set == j, 0], x_set[y_set == j, 1], c = ListedColormap(('blue', 'orange'))(i), label = j, edgecolors='black')
plt.title('SVM (Test Set)')
plt.xlabel('Sensor')
plt.ylabel('Time')
#plt.figure(figsize=(40,20))
plt.legend()
plt.show()