from flask import Flask, request, jsonify
import pandas as pd
from flask_cors import CORS
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import numpy as np

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


@app.route('/', methods=['GET'])
def index():
    return 'Machine learning service!'


def prep_data(attacker, defender):
    # Prepare feature data frames
    attacker_features = {k: v for k, v in attacker.items() if k != 'WL'}
    defender_features = {k: v for k, v in defender.items() if k != 'WL'}
    attack_features_df = pd.DataFrame([attacker_features])
    defender_features_df = pd.DataFrame([defender_features])

    expanded_df = pd.DataFrame()

    for column in ['KD', 'HS', 'KPR']:
        temp_df = pd.DataFrame.from_dict(attack_features_df[column][0], orient='index', columns=[column])
        temp_df['Name'] = attack_features_df['Name'][0]
        temp_df.reset_index(inplace=True)
        temp_df.rename(columns={'index': 'Measurement'}, inplace=True)
        if expanded_df.empty:
            expanded_df = temp_df
        else:
            expanded_df = pd.merge(expanded_df, temp_df, on=['Name', 'Measurement'], how='outer')

    expanded_df1 = pd.DataFrame()

    for column in ['KD', 'HS', 'KPR']:
        temp_df = pd.DataFrame.from_dict(defender_features_df[column][0], orient='index', columns=[column])
        temp_df['Name'] = defender_features_df['Name'][0]
        temp_df.reset_index(inplace=True)
        temp_df.rename(columns={'index': 'Measurement'}, inplace=True)
        if expanded_df1.empty:
            expanded_df1 = temp_df
        else:
            expanded_df1 = pd.merge(expanded_df1, temp_df, on=['Name', 'Measurement'], how='outer')

    # Prepare target values
    y_a = np.array([attacker['WL']])
    y_d = np.array([defender['WL']])

    dictionary = y_a[0]
    dictionary1 = y_d[0]

    y_attack = pd.DataFrame(list(dictionary.items()), columns=['Measurement', 'Value'])['Value'].to_numpy()
    y_defend = pd.DataFrame(list(dictionary1.items()), columns=['Measurement', 'Value'])['Value'].to_numpy()
    X_attack = expanded_df.drop('Name', axis=1).to_numpy()
    X_defend = expanded_df1.drop('Name', axis=1).to_numpy()

    X_attack_train, X_attack_test, y_attack_train, y_attack_test = train_test_split(X_attack, y_attack, test_size=0.2,
                                                                                    random_state=42)
    X_defend_train, X_defend_test, y_defend_train, y_defend_test = train_test_split(X_defend, y_defend, test_size=0.2,
                                                                                    random_state=42)

    # Initialize and train the Random Forest Regressor
    model_attack = RandomForestRegressor(n_estimators=100, random_state=42)
    model_defend = RandomForestRegressor(n_estimators=100, random_state=42)
    model_attack.fit(X_attack_train, y_attack_train)
    model_defend.fit(X_defend_train, y_defend_train)

    # Make predictions
    y_attack_pred = model_attack.predict(X_attack_test)
    y_defend_pred = model_defend.predict(X_defend_test)

    mse_attack = mean_squared_error(y_attack_test, y_attack_pred)
    mse_defend = mean_squared_error(y_defend_test, y_defend_pred)

    return mse_attack, mse_defend


@app.route('/accept_data', methods=['POST', 'GET'])
def accept_data():
    if request.is_json:
        data = request.get_json()
        attacker_data = data.get('Attacker', {})
        defender_data = data.get('Defender', {})
        mse_a, mse_d = prep_data(attacker_data, defender_data)
        return jsonify({"mseAttack": mse_a,
                        "mseDefend": mse_d}), 200
    else:
        return jsonify({"error": "Request must be JSON"}), 400


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3001)
