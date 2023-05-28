import pandas as pd

from xgboost import XGBClassifier

from sklearn.metrics import accuracy_score, recall_score, precision_score, f1_score
from sklearn.model_selection import train_test_split

genres = ['folk', 'rock', 'pop', 'indie', 'hip hop', 'r&b', 'trap', 'latin', 'rap', 'classical']


def prepare_tracks(tracks, artists):
    tracks_df = pd.read_json(tracks, lines=True)
    tracks_df = tracks_df[~tracks_df['mode'].isna()]

    artists_df = pd.read_json(artists, lines=True)

    for genre in genres:
        artists_df[genre] = artists_df.genres.apply(lambda x: 1 if genre in str(x) else 0)

    artists_df = artists_df.drop(columns=['name', 'genres'])

    final_df = tracks_df.merge(artists_df, left_on='id_artist', right_on='id')
    final_df = pd.get_dummies(final_df, columns=['key'])


    return final_df

def split(final_df):
    X_train_final, X_test_final, y_train, y_test = train_test_split(
        final_df.drop(columns=['mode', 'name', 'id_x', 'id_y', 'id_artist',
                                'release_date', 'explicit', 'time_signature']),
        final_df['mode'],
        test_size=0.2,
        random_state=42
    )

    return X_train_final, X_test_final, y_train, y_test

def evaluate_model(model: XGBClassifier,
                   X_train: pd.DataFrame,
                   X_test: pd.DataFrame,
                   y_train: pd.DataFrame,
                   y_test: pd.Series,
                   is_for_stats=False) -> None:
    
    model.fit(X_train, y_train)
    preds = model.predict(X_test)

    if not is_for_stats:
        return preds
    else:
        return preds, y_test

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
