from flask import Flask, render_template, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/messages', methods=['GET'])
def get_messages():
    # JSONArray
    messages = [ # dictionary list
        {
            'id': 1,
            'channel_id': 1,
            'user_id': 1,
            'text': 'hello, world!',
            'creation_ts': '2025-04-10 22:04:34'
        },
        {
            'id': 2,
            'channel_id': 1,
            'user_id': 1,
            'text': 'how you doin?',
            'creation_ts': '2025-04-10 22:04:34'
        },
        {
            'id': 3,
            'channel_id': 1,
            'user_id': 1,
            'text': 'hi',
            'creation_ts': '2025-04-10 22:04:34'
        }
    ]
    return jsonify(messages) # Formato JSONObject ou JSONArray
