from flask import Flask,jsonify,request

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
def validate_game(data):
    if not isinstance(data, dict):
        return "Нужно передать JSON-объект"

    for field in ("title", "genre", "platform"):
        value = data.get(field)
        if not isinstance(value, str) or not value.strip():
            return f"Поле {field} должно быть непустой строкой"
    rating = data.get("rating")
    if type(rating) not in (int, float) or not 0 <= rating <= 10:
        return "Рейтинг должен быть числом от 0 до 10"
    return None
if __name__ == '__main__':
    app.run(port=3000, debug=True)