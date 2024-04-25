from flask import Flask, request, jsonify
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return 'Machine learning service!'


def prep_data(attacker, defender):
    # Prepare feature data frames
    attacker_features = {k: v for k, v in attacker.items() if k != 'WL'}
    defender_features = {k: v for k, v in defender.items() if k != 'WL'}
    attack_features_df = pd.DataFrame([attacker_features])
    defender_features_df = pd.DataFrame([defender_features])

    # Prepare target values
    y_attack = np.array([attacker['WL']])
    y_defend = np.array([defender['WL']])

    X_attack = attack_features_df.to_numpy()
    X_defend = defender_features_df.to_numpy()

    print("Attack Features:\n", attack_features_df)
    print("Defend Features:\n", defender_features_df)
    print("Attack WL:", y_attack)
    print("Defend WL:", y_defend)

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
    print("Attacker Model R^2 Score:", r2_score(y_attack, y_attack_pred))
    print("Defender Model R^2 Score:", r2_score(y_defend, y_defend_pred))


@app.route('/accept_data', methods=['POST', 'GET'])
def accept_data():
    attacker_mock = {
        'WL': 0.75,
        'KD': 1.3,
        'HS': 0.7,
        'KPR': 0.3
    }
    defender_mock = {
        'WL': 0.65,
        'KD': 1.1,
        'HS': 0.6,
        'KPR': 0.25
    }
    if request.is_json:
        data = request.get_json()
        print("Received data:")
        attacker_data = data.get('Attacker', {})
        defender_data = data.get('Defender', {})
        prep_data(attacker_data, defender_data)
        return jsonify({"message": "Data received successfully"}), 200
    else:
        prep_data(attacker_mock, defender_mock)
        return jsonify({"error": "Request must be JSON"}), 400


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3001)
