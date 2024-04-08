import asyncio
from siegeapi import Auth
from flask import Flask, request, jsonify
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

        # Collect data in a dictionary to return
        player_data = {
            "Name": player.name,
            "TotalTimePlayedSeconds": player.total_time_played,
            "Level": player.level
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
    app.run(debug=True, host='0.0.0.0', port=5000)
