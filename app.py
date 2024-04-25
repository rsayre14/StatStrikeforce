import asyncio
import aiohttp
from siegeapi import Auth
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
from database import Database

app = Flask(__name__)
load_dotenv()
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default_secret_key')
DATABASE = os.environ.get('DATABASE')
MACHINE_LEARNING = os.environ.get('MACHINE_LEARNING')
db = Database(app, DATABASE)
app.extensions['database'] = db


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
    loop.run_until_complete(send_data(player_data))
    loop.close()

    return jsonify(player_data)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)
