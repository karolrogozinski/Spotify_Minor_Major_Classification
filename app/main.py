# from flask import Flask
from flask import Flask, jsonify, request, send_file
import BaseModel
import FinalModel
from flask_cors import CORS
import io
from copy import deepcopy
import shutil

from xgboost import XGBClassifier

app = Flask(__name__)
CORS(app)

def name_preds(preds):
    preds_names = []

    for pred in preds:
        if pred == 1:
            preds_names.append('dur')
        elif pred == 0:
            preds_names.append('moll')
        else:
            preds_names.append('błędna predykcja')

    return preds_names

def evaluate_base_model(tracks, is_for_stats=False):
    tracks_df = BaseModel.prepare_tracks(file=tracks)
    X_train, X_test, y_train, y_test = BaseModel.split(tracks_df)
    
    return BaseModel.evaluate_model(XGBClassifier(), X_train, X_test, y_train, y_test, is_for_stats)


def evaluate_final_model(tracks, artists, is_for_stats=False):
    tracks_df = FinalModel.prepare_tracks(tracks, artists)
    X_train_final, X_test_final, y_train, y_test = FinalModel.split(tracks_df)

    best_params = {'eta': 0.1, 'max_depth': 7, 'n_estimators': 50}

    return FinalModel.evaluate_model(XGBClassifier(**best_params), X_train_final, X_test_final, y_train, y_test, is_for_stats)

    

@app.route('/get-base-predictions', methods=['POST'])
def get_base_predictions():

    file = request.files['file']
    if not file:
        return None
    prediction_results = name_preds(evaluate_base_model(file))

    file_path = 'base_model_predictions.txt'
    with open(file_path, 'w') as f:
        for prediction in prediction_results:
            f.write(prediction + '\n')

    data = io.BytesIO()
    with open(file_path, 'rb') as f:
        data.write(f.read())
    data.seek(0)

    response = send_file(data, mimetype='text/plain', as_attachment=True, download_name='base_model_predictions.txt')

    response.headers['Content-Disposition'] = 'attachment; filename=file.txt'
    response.headers['Cache-Control'] = 'no-cache'

    return response

@app.route('/get-final-predictions', methods=['POST'])
def get_final_predictions():

    tracks = request.files['tracks']
    artists = request.files['artists']

    if not tracks or not artists:
        return None
    
    prediction_results = name_preds(evaluate_final_model(tracks, artists))

    file_path = 'final_model_predictions.txt'
    with open(file_path, 'w') as f:
        for prediction in prediction_results:
            f.write(prediction + '\n')

    data = io.BytesIO()
    with open(file_path, 'rb') as f:
        data.write(f.read())
    data.seek(0)

    response = send_file(data, mimetype='text/plain', as_attachment=True, download_name='final_model_predictions.txt')

    response.headers['Content-Disposition'] = 'attachment; filename=file.txt'
    response.headers['Cache-Control'] = 'no-cache'

    return response

@app.route('/experiment', methods=['POST'])
def experiment():
    tracks = request.files['tracks']
    tracks2 = io.BytesIO(tracks.read())
    tracks2.seek(0)
    tracks.seek(0)
    artists = request.files['artists']

    if not tracks or not artists:
        return None
    
    base_preds, base_y_test = evaluate_base_model(tracks, True)
    base_stats = BaseModel.get_stats(base_preds, base_y_test)

    # base_stats=[',']

    final_preds, final_y_test = evaluate_final_model(tracks2, artists, True)
    final_stats = FinalModel.get_stats(final_preds, final_y_test)

    return jsonify({'baseStats': base_stats, 'finalStats': final_stats})

    # base_tracks_df = BaseModel.prepare_tracks(tracks)
    # bX_train, bX_test, by_train, by_test = BaseModel.split(base_tracks_df)
    # base_preds = BaseModel.evaluate_model(XGBClassifier(), bX_train, bX_test, by_train, by_test)
    # base_stats = BaseModel.get_stats(base_preds, by_test)

    # final_stats = ['a', 'b']
    # final_tracks_df = FinalModel.prepare_tracks(tracks, artists)
    # X_train_final, X_test_final, fy_train, fy_test = FinalModel.split(final_tracks_df)
    # best_params = {'eta': 0.1, 'max_depth': 7, 'n_estimators': 50}
    # final_preds = FinalModel.evaluate_model(XGBClassifier(**best_params), X_train_final, X_test_final, fy_train, fy_test)
    # final_stats = FinalModel.get_stats(final_preds, fy_test)

    return jsonify({'base_stats': base_stats, 'final_stats': final_stats})    

if __name__ == '__main__':

    app.run()