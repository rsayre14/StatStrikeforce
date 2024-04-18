import asyncio
from siegeapi import Auth
from flask import Flask, request, jsonify
import json
import pprint
from dotenv import load_dotenv
import os
from database import Database

app = Flask(__name__)
load_dotenv()
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default_secret_key')
DATABASE = os.environ.get('DATABASE')
db = Database(app, DATABASE)
app.extensions['database'] = db


@app.route('/')
def backend_world():
    return 'Group 3 Backend!'


async def sample(user_id):
    try:
        auth = Auth(os.getenv('UBI_EMAIL'), os.getenv('UBI_PASSWORD'))
        player = await auth.get_player(uid=user_id)

        await player.load_playtime()

        await player.load_operators()
        await player.load_maps()
        await player.load_trends()
        await player.load_weapons()

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
            "Name": player.name,
            "TotalTimePlayedSeconds": player.total_time_played,
            "AttackerMapStats": map_stats_attacker,
            "DefenderMapStats": map_stats_defender,
            "TrendDefenderStats": player.trends.ranked.defender.win_loss_ratio.trend,
            "TrendAttackerStats": player.trends.ranked.attacker.win_loss_ratio.trend
        }

        await auth.close()

        return player_data
    except Exception as e:
        print(e)


@app.route('/get_rainbow_stats', methods=['GET'])
def get_rainbow_stats():
    user_id = request.args.get('uid')

    # This runs the async function and waits for a response
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    player_data = loop.run_until_complete(sample(user_id))
    loop.close()

    return jsonify(player_data)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)
