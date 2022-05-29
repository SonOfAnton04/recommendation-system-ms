import os
import numpy as np
import pandas as pd
from flask import Flask, request, g, jsonify
from flask_cors import CORS, cross_origin
from config import BaseConfig
from helper import user_based_prediction, item_based_prediction

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UI_FOLDER = os.path.join(APP_ROOT, 'ui')
app = Flask(__name__, static_url_path="", static_folder=UI_FOLDER)

def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'PUT,GET,POST,DELETE'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
    return response

app.after_request(after_request)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/api/v1/genres', methods=['GET'])
@cross_origin()
def get_genres():
    return jsonify(list(BaseConfig.GENRES.keys()))

@app.route('/api/v1/user/', methods=['GET'])
@cross_origin()
def get_user_based_prediction():
    print("in get_user_based_prediction")
    args = request.args
    distance = args.get('distance', 'pearson')
    user_item_df = pd.read_csv('./ml-latest-small/user_item.csv')
    movies = user_based_prediction(user_item_df, distance)
    
    return jsonify(movies)

@app.route('/api/v1/item/', methods=['GET'])
@cross_origin()
def get_item_based_prediction():
    args = request.args
    distance = args.get('distance', 'pearson')
    user_item_df = pd.read_csv('./ml-latest-small/user_item.csv')
    movies = item_based_prediction(user_item_df, distance)
    
    return jsonify(movies)


def main():
    app.run(debug=True)

if __name__ == '__main__':
    main()
    
