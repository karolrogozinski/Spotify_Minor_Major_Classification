# from flask import Flask
from flask import Flask, render_template, send_from_directory, request
import os
import BaseModel
from flask_cors import CORS


from xgboost import XGBClassifier

app = Flask(__name__)
CORS(app)


@app.route('/')
def hello():
    return 'Witaj w mojej aplikacji!'

@app.route('/base')
# @app.route('/get-prediction', methods=['GET'])
def evaluate_base_model():
    X_train, X_test, y_train, y_test = BaseModel.split()
    preds = BaseModel.evaluate_model(XGBClassifier(), X_train, X_test, y_train, y_test)

    return name_prediction(preds[0])

def name_prediction(pred_value):
    phrase = 'Utwór przewidziany jako: '
    if int(pred_value) == 1:
        end = 'DUROWY.'
    elif int(pred_value) == 0:
        end = 'MOLOWY.'
    else:
        end = "DURNOTA."
    
    return phrase + end

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/static/<path:path>')
def static_proxy(path):
    # Przekierowanie żądań dla plików statycznych
    static_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'build', 'static')
    return send_from_directory(static_folder, path)

@app.route('/get-prediction', methods=['POST'])
def get_prediction():
    # number = request.json.get('number')
    prediction_result = evaluate_base_model() #name_prediction(number)
    return { 'result': prediction_result}

if __name__ == '__main__':

    app.run()