import asyncio
import aiohttp
from siegeapi import Auth
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
import bcrypt
from database import Database

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
load_dotenv()
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default_secret_key')
DATABASE = os.environ.get('DATABASE')
MACHINE_LEARNING = os.environ.get('MACHINE_LEARNING')
db = Database(app, DATABASE)
app.extensions['database'] = db


def initialize_database():
    db.init_db()


# endpoint
@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    r6_user_id = data.get('r6Account')  # Use .get() to avoid KeyError

    if not username or not password or not r6_user_id:
        return jsonify({"success": False, "message": "Missing required fields"}), 400

    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    db.query_db(
        "INSERT INTO user (username, password_hash, r6_user_id) VALUES (?, ?, ?)",
        [username, password_hash, r6_user_id],
    )

    return jsonify({"success": True, "message": "User created successfully"}), 201


# Endpoint for login
@app.route('/login', methods=['POST'])  # Added login endpoint
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    user = db.query_db(
        "SELECT * FROM user WHERE username = ?", [username], one=True
    )

    # Check password against hash
    if user and bcrypt.checkpw(password.encode('utf-8'), user['password_hash']):
        return jsonify({"success": True, "message": "Login successful"}), 200
    else:
        return jsonify({"success": False, "message": "Invalid username or password"}), 401


@app.route('/')
def backend_world():
    return 'Group 3 Backend!'


async def sample(user_id1, user_id2):
    try:
        auth = Auth(os.getenv('UBI_EMAIL'), os.getenv('UBI_PASSWORD'))
        player = await auth.get_player(uid=user_id1)
        player2 = await auth.get_player(uid=user_id2)

        await player.load_maps()
        await player.load_trends()

        await player2.load_trends()

        map_stats_defender = []
        map_stats_attacker = []

        for map_object in player.maps.all.defender:
            stats = {
                "Map Name": map_object.map_name,
                "Matches Won": map_object.matches_won,
                "Matches Lost": map_object.matches_lost,
                "Rounds Won": map_object.rounds_won,
                "Rounds Lost": map_object.rounds_lost,
                "Win/Loss Ratio": map_object.win_loss_ratio,
                "Headshot Accuracy": map_object.headshot_accuracy,
                "Kill/Death Ratio": map_object.kill_death_ratio,
                "Rounds with an Ace": map_object.rounds_with_an_ace
            }
            map_stats_defender.append(stats)

        for map_object in player.maps.all.attacker:
            stats = {
                "Map Name": map_object.map_name,
                "Matches Won": map_object.matches_won,
                "Matches Lost": map_object.matches_lost,
                "Rounds Won": map_object.rounds_won,
                "Rounds Lost": map_object.rounds_lost,
                "Win/Loss Ratio": map_object.win_loss_ratio,
                "Headshot Accuracy": map_object.headshot_accuracy,
                "Kill/Death Ratio": map_object.kill_death_ratio,
                "Rounds with an Ace": map_object.rounds_with_an_ace
            }
            map_stats_attacker.append(stats)

        player_data = {
            "Attacker": {
                "Name": player.name,
                "WL": player.trends.ranked.attacker.win_loss_ratio.trend,
                "KD": player.trends.ranked.attacker.kill_death_ratio.trend,
                "HS": player.trends.ranked.attacker.headshot_accuracy.trend,
                "KPR": player.trends.ranked.attacker.kills_per_round.trend,
            },
            "Defender": {
                "Name": player2.name,
                "WL": player2.trends.ranked.defender.win_loss_ratio.trend,
                "KD": player2.trends.ranked.defender.kill_death_ratio.trend,
                "HS": player2.trends.ranked.defender.headshot_accuracy.trend,
                "KPR": player2.trends.ranked.defender.kills_per_round.trend,
            }
        }
        await auth.close()

        return player_data
    except Exception as e:
        print(e)


async def send_data(player_data):
    async with aiohttp.ClientSession() as session:
        headers = {'Content-Type': 'application/json'}
        async with session.post(MACHINE_LEARNING, json=player_data, headers=headers) as response:
            if response.status == 200:
                print('Data sent successfully')
                response_data = await response.json()
                mse_attack = response_data.get("mseAttack")
                mse_defend = response_data.get("mseDefend")
                print(f"MSE Attack: {mse_attack}, MSE Defend: {mse_defend}")
                return response_data
            else:
                print('Failed to send data', await response.text())


@app.route('/get_rainbow_stats', methods=['GET'])
def get_rainbow_stats():
    user_id_1 = request.args.get('uid1')
    user_id_2 = request.args.get('uid2')

    # This runs the async function and waits for a response
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    player_data = loop.run_until_complete(sample(user_id_1, user_id_2))
    predictions = loop.run_until_complete(send_data(player_data))
    loop.close()

    sql = """
    INSERT INTO user_stats (user_id, mse_attack, mse_defend)
    VALUES (?, ?, ?)
    ON CONFLICT(user_id) DO UPDATE SET
        mse_attack = COALESCE(?, mse_attack),
        mse_defend = COALESCE(?, mse_defend)
    """

    db.query_db(sql, [
        user_id_1,
        predictions.get('mseAttack'),
        None,
        predictions.get('mseAttack'),
        None
    ])

    db.query_db(sql, [
        user_id_2,
        None,
        predictions.get('mseDefend'),
        None,
        predictions.get('mseDefend')
    ])

    return jsonify(player_data=player_data, predictions=predictions)


if __name__ == '__main__':
    initialize_database()
    app.run(debug=True, host='0.0.0.0', port=3000)
