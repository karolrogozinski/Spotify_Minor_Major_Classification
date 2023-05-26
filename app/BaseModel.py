import pandas as pd

from xgboost import XGBClassifier

from sklearn.metrics import accuracy_score, recall_score, precision_score, f1_score
from sklearn.model_selection import train_test_split


tracks_df = pd.read_json('../data/tracks.jsonl', lines=True)
tracks_df = tracks_df[~tracks_df['mode'].isna()]

def split():
    X_train, X_test, y_train, y_test = train_test_split(
        tracks_df.drop(columns=['mode', 'id', 'name', 'id_artist', 'release_date']),
        tracks_df['mode'],
        test_size=0.2,
        random_state=42
    )
    
    return X_train, X_test, y_train, y_test

def evaluate_model(model: XGBClassifier,
                   X_train: pd.DataFrame,
                   X_test: pd.DataFrame,
                   y_train: pd.DataFrame,
                   y_test: pd.Series) -> None:
    
    model.fit(X_train, y_train)
    preds = model.predict(X_test)

    return preds

    # print('Accuracy:', accuracy_score(y_test, preds))
    # print('Recall:', recall_score(y_test, preds))
    # print('Precision:',precision_score(y_test, preds))
    # print('F1:',f1_score(y_test, preds))
    # print()
    # print('Predicted class balance:')
    # print(pd.Series(preds).value_counts()/len(preds)*100)
    # print()
    # print('Original:')
    # print(y_test.value_counts()/y_test.shape[0]*100)

# X_train, X_test, y_train, y_test = split()
# evaluate_model(XGBClassifier(), X_train, X_test, y_train, y_test)

