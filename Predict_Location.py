# -*- coding: utf-8 -*-
"""
Created on Sat Nov 17 12:34:14 2018

@author: Trey
"""
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import AdaBoostClassifier
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.metrics import accuracy_score
import random

CLEAN_DATA_FILENAME = "Clean_Data.csv"
PREPROCESSING = False

if PREPROCESSING:
    data = pd.read_csv(CLEAN_DATA_FILENAME)
    
    data = data.drop(["Priority", "Call_Year"], axis=1)
    
    # Divide zone into four regions
    to_drop = []
    for index, row in data.iterrows():
        if row["Zone"] == 'UNK':
            to_drop.append(index)
        else:
            data.at[index, "Zone"] = int(str(data.at[index, "Zone"])[0])
    
    data.drop(to_drop, axis=0, inplace=True)
    print("Done preprocessing")

## Divide dataset to make training more tractable
#indices = list(data.index.values)
#random.shuffle(indices)
#
#small_data = data.loc[indices[:len(indices) // 4]]
#
#X = small_data[["Call_Date", "Call_Month", "Call_Time"]]
#y = small_data["Zone"]
#y = y.astype(int)
#

X = data[["Call_Date", "Call_Month", "Call_Time"]]
y = data["Zone"].astype(int)

X = pd.get_dummies(X, columns=["Call_Date", "Call_Month", "Call_Time"])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
print("Split data")
dt = DecisionTreeClassifier(random_state = 42)
#log = LogisticRegression(random_state=42)
#clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf = AdaBoostClassifier(dt)

print(cross_val_score(clf, X_train, y_train, cv=2))
#print("Fitting Classifier...")
#clf.fit(X_train, y_train)
#print("Fit Classifier")
#y_pred = clf.predict(X_train)
#print(accuracy_score(y_train, y_pred))