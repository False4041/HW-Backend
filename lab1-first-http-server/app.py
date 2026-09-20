from flask import Flask, jsonify,request
import time

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello, server works!'
@app.route('/api/matches')
def matches():
    return jsonify([
        {"id": 1, "team1": "Spartak", "team2": "Zenit"},
        {"id": 2, "team1": "CSKA", "team2": "Dynamo"}
    ])
@app.route('/api/teams')
def teams():
    return jsonify([
        {"id": 1, "name": "Spartak"},
        {"id": 2, "name": "Zenit"},
        {"id": 3, "name": "CSKA"},
        {"id": 4, "name": "Dynamo"}
    ])
@app.route('/api/matches/<int:match_id>')
def match_by_id(match_id):
    return jsonify({
        "requestedId": match_id,
        "status": "success"
    })
@app.errorhandler(404)
def page_not_found(error):
    return jsonify({
        "error": "Not Found"
    }), 404
@app.before_request
def log_request():
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {request.method} {request.path}")
app.run(port=3000)
if __name__ == '__main__':
    app.run(port=3000, debug=True)