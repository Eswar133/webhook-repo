from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)

# MongoDB connection
client = MongoClient('mongodb+srv://manikantapadala358:2RQG5wTO8igTrCqk@cluster0.sntr3.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
db = client['github_actions']
collection = db['actions']

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    action = data.get('action')
    author = data.get('sender', {}).get('login')
    timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')

    if action == 'push':
        from_branch = data.get('ref').split('/')[-1]
        to_branch = from_branch  # For push, from and to branches are the same
        event = {
            'request_id': data.get('head_commit', {}).get('id'),
            'author': author,
            'action': 'PUSH',
            'from_branch': from_branch,
            'to_branch': to_branch,
            'timestamp': timestamp
        }
    elif action == 'pull_request':
        pr_data = data.get('pull_request', {})
        from_branch = pr_data.get('head', {}).get('ref')
        to_branch = pr_data.get('base', {}).get('ref')
        event = {
            'request_id': str(pr_data.get('id')),
            'author': author,
            'action': 'PULL_REQUEST',
            'from_branch': from_branch,
            'to_branch': to_branch,
            'timestamp': timestamp
        }
    elif action == 'merge':
        pr_data = data.get('pull_request', {})
        from_branch = pr_data.get('head', {}).get('ref')
        to_branch = pr_data.get('base', {}).get('ref')
        event = {
            'request_id': str(pr_data.get('id')),
            'author': author,
            'action': 'MERGE',
            'from_branch': from_branch,
            'to_branch': to_branch,
            'timestamp': timestamp
        }
    else:
        return jsonify({'status': 'unknown action'}), 400

    # Insert event into MongoDB
    collection.insert_one(event)
    return jsonify({'status': 'success'}), 200

@app.route('/latest_actions', methods=['GET'])
def latest_actions():
    # Fetch the latest 10 actions from MongoDB
    actions = list(collection.find().sort('timestamp', -1).limit(10))
    for action in actions:
        action['_id'] = str(action['_id'])  # Convert ObjectId to string
    return jsonify(actions)

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(port=5000)