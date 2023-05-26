import pandas as pd

from xgboost import XGBClassifier

from sklearn.metrics import accuracy_score, recall_score, precision_score, f1_score
from sklearn.model_selection import train_test_split

def prepare_tracks(file):
    tracks_df = pd.read_json(file, lines=True)
    tracks_df = tracks_df[~tracks_df['mode'].isna()]
    return tracks_df


def split(tracks_df):
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

def get_stats(preds, y_test):
    stats = []
    stats.append(f'Accuracy: {accuracy_score(y_test, preds)}')
    stats.append(f'Recall: {recall_score(y_test, preds)}')
    stats.append(f'Precision: {precision_score(y_test, preds)}')
    stats.append(f'F1: {f1_score(y_test, preds)}')
    stats.append('')
    stats.append(f'Predicted class balance:')
    stats.append(f'{pd.Series(preds).value_counts()/len(preds)*100}')
    stats.append('')
    stats.append(f'Original:')
    stats.append(f'{y_test.value_counts()/y_test.shape[0]*100}')

    return stats
