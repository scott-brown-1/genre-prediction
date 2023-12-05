#import os
#os.chdir('..')
#print(os.getcwd())

import warnings
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import SMOTE

from constants import DATA_DIR, DROP_COLS

TARGET = 'Genre'

## Create train test split breaking on artist_id
def artist_train_test_split(df, test_size = 0.3):
    ## Get unique artist ids and randomize order
    artist_ids = df['artist_id'].unique()
    np.random.shuffle(artist_ids)

    ## Get indices of test and train
    split = int(len(artist_ids) * test_size)
    test_artist_ids = artist_ids[:split]
    train_artist_ids = artist_ids[split:]

    ## Get train and test df
    train = df[df['artist_id'].isin(train_artist_ids)]
    test = df[df['artist_id'].isin(test_artist_ids)]

    ## Drop artist_id from train and test
    train = train.drop('artist_id', axis=1)
    test = test.drop('artist_id', axis=1)
    
    return train, test

def load_train_test(scale=False, upsample=True, encode=False):
    data = pd.read_csv(f'{DATA_DIR}/Final_Data_For_Real.csv')

    ## Prepare data for modeling
    data = data.drop(DROP_COLS, axis=1)

    ## Shuffle data
    data = data.sample(frac=1, random_state=42)

    ## Convert string columns to categorical
    # TODO: Target encode! This defaults to one-hot
    for col in data.columns:
        if (data[col].dtype == 'object' and 
            col != TARGET and
            col != 'artist_id'):
            data[col] = data[col].astype('category')

    data['time_signature'] = data['time_signature'].astype('category')

    train, test = artist_train_test_split(data, test_size=0.3)

    ## Split train and test into X_train, X_test, y_train, y_test
    X_train = train.drop(TARGET,axis=1)
    y_train = train[TARGET]

    X_test = test.drop(TARGET,axis=1)
    y_test = test[TARGET]

    #X = data.drop(TARGET,axis=1)
    #y = data[TARGET]

    if(upsample):
        print('Upsampling data not yet implemented')
        sm = SMOTE(random_state=42)
        X_train, y_train = sm.fit_resample(X_train, y_train)

    #X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3, random_state = 0)

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

    

