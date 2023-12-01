import warnings
import pandas as pd
from sklearn.metrics import accuracy_score

def predict_and_evaluate(model, new_data, truth_data):
    ## Predict new data
    y_pred = pd.DataFrame(model.predict(new_data))
    y_prob = pd.DataFrame(model.predict_proba(new_data), columns=model.classes_)

    ## Calculate accuracy of predicting top genre
    top_genre_accuracy = accuracy_score(truth_data.apply(lambda x: x[0]), y_pred)
    print(f'Top genre accuracy: {top_genre_accuracy}')

    ## Calculate accuracy of predicting all genres
    total_correct = 0
    total_genres = 0

    for i,genres in enumerate(truth_data):
        top_k_preds = y_prob.loc[i,:].nlargest(len(genres)).index.tolist()

        # Count the number of correct predictions
        correct_preds = len(set(top_k_preds).intersection(set(genres)))
        total_correct += correct_preds
        total_genres += len(genres)
        
        #accuracy = correct_preds / len(genres)
        #print(f'Accuracy for {i}: {accuracy}')
    
    all_genre_accuracy = total_correct / total_genres
    print(f'All genre accuracy: {all_genre_accuracy}')

    return y_pred, y_prob