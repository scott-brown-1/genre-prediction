#import os
#os.chdir('..')
#print(os.getcwd())

import warnings
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import SMOTE

from constants import DATA_DIR, DROP_COLS

TARGET = 'Genre'

def load_train_test(scale=False, upsample=True, encode=False):
    data = pd.read_csv(f'{DATA_DIR}/Final_Data_For_Real.csv')

    ## Prepare data for modeling
    data = data.drop(DROP_COLS, axis=1)

    ## Convert string columns to categorical
    # TODO: Target encode! This defaults to one-hot
    for col in data.columns:
        if data[col].dtype == 'object' and col != TARGET:
            data[col] = data[col].astype('category')

    data['time_signature'] = data['time_signature'].astype('category')

    X = data.drop(TARGET,axis=1)
    y = data[TARGET]

    if(upsample):
        sm = SMOTE(random_state=42)
        X, y = sm.fit_resample(X, y)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3, random_state = 0)

    ## Manual one-hot encoding
    if(encode):
        X_train = pd.get_dummies(X_train, drop_first=True)
        X_test = pd.get_dummies(X_test, drop_first=True)

    # Feature scaling
    if(scale):
        sc = StandardScaler()
        X_train = sc.fit_transform(X_train)
        X_test = sc.transform(X_test)

    y_train = y_train.str.findall(r"'(.*?)'").apply(lambda x: x[0])
    y_test = y_test.str.findall(r"'(.*?)'")
        
    return X_train, X_test, y_train, y_test

    

