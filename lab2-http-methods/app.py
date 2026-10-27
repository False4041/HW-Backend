from flask import Flask,jsonify

app = Flask(__name__)
games = [
    {"id": 1, "title": "Minecraft", "genre": "Sandbox", "platform": "PC", "rating": 9.0},
    {"id": 2, "title": "Portal 2", "genre": "Puzzle", "platform": "PC", "rating": 9.5},
    {"id": 3, "title": "God of War", "genre": "Action", "platform": "PlayStation", "rating": 9.1}
]
@app.route('/games', methods=['GET'])
def get_games():
    return jsonify({
        "count": len(games),
        "games": games
    })
@app.route('/games/<int:game_id>', methods=['GET'])
def get_game(game_id):
    for game in games:
        if game["id"] == game_id:
            return jsonify(game)

    return jsonify({"error": "Игра не найдена"}), 404
if __name__ == '__main__':
    app.run(port=3000, debug=True)