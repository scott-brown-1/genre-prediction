import warnings
import pandas as pd
from sklearn.metrics import accuracy_score

def predict_and_evaluate(model, new_data, truth_data, multilabel=False):
    if(multilabel):
        #warnings.warn('Multi-label classification not yet supported. Returning single-label data.')
        #y_pred = predict_and_evaluate(model, new_data, truth_data, multilabel=False)
        #return y_pred
        y_pred = model.predict_proba(new_data)
    else:
        truth_data = truth_data.str.findall(r"'(.*?)'").apply(lambda x: x[0])
        y_pred = model.predict(new_data)
        accuracy = accuracy_score(truth_data, y_pred)

    #print(accuracy)
    return y_pred