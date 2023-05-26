import pandas as pd

from xgboost import XGBClassifier

from sklearn.metrics import accuracy_score, recall_score, precision_score, f1_score
from sklearn.model_selection import train_test_split

genres = ['folk', 'rock', 'pop', 'indie', 'hip hop', 'r&b', 'trap', 'latin', 'rap', 'classical']


tracks_df = pd.read_json('./data/tracks.jsonl', lines=True)
tracks_df = tracks_df[~tracks_df['mode'].isna()]

artists_df = pd.read_json('./data/artists.jsonl', lines=True)

def evaluate_model(model: XGBClassifier,
                   X_train: pd.DataFrame,
                   X_test: pd.DataFrame,
                   y_train: pd.DataFrame,
                   y_test: pd.Series) -> None:
    
    model.fit(X_train, y_train)
    preds = model.predict(X_test)

    print('Accuracy:', accuracy_score(y_test, preds))
    print('Recall:', recall_score(y_test, preds))
    print('Precision:',precision_score(y_test, preds))
    print('F1:',f1_score(y_test, preds))
    print()
    print('Predicted class balance:')
    print(pd.Series(preds).value_counts()/len(preds)*100)
    print()
    print('Original:')
    print(y_test.value_counts()/y_test.shape[0]*100)


for genre in genres:
    artists_df[genre] = artists_df.genres.apply(lambda x: 1 if genre in str(x) else 0)

artists_df = artists_df.drop(columns=['name', 'genres'])

final_df = tracks_df.merge(artists_df, left_on='id_artist', right_on='id')
final_df = pd.get_dummies(final_df, columns=['key'])

X_train_final, X_test_final, y_train, y_test = train_test_split(
    final_df.drop(columns=['mode', 'name', 'id_x', 'id_y', 'id_artist',
                            'release_date', 'explicit', 'time_signature']),
    final_df['mode'],
    test_size=0.2,
    random_state=42
)

best_params = {'eta': 0.1, 'max_depth': 7, 'n_estimators': 50}

evaluate_model(XGBClassifier(**best_params), X_train_final, X_test_final, y_train, y_test)



