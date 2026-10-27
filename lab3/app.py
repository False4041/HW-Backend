from flask import Flask, jsonify

app = Flask(__name__)
app.json.ensure_ascii = False

games = [
    {"id": 1, "title": "Minecraft", "genre": "Sandbox", "platform": "PC"},
    {"id": 2, "title": "Portal 2", "genre": "Puzzle", "platform": "PC"},
    {"id": 3, "title": "God of War", "genre": "Action", "platform": "PlayStation"}
]

reviews = {
    1: [{"id": 1, "text": "Можно строить собственные миры."}],
    2: [{"id": 2, "text": "Интересные головоломки с порталами."}],
    3: []
}


def parse_id(value):
    try:
        number = int(value)
    except ValueError:
        return None
    if number < 1:
        return None
    return number


def find_game(game_id):
    for game in games:
        if game["id"] == game_id:
            return game
    return None


@app.route('/games', methods=['GET'])
def get_games():
    return jsonify({"count": len(games), "games": games}), 200


@app.route('/games/<game_id>', methods=['GET'])
def get_game(game_id):
    game_id = parse_id(game_id)
    if game_id is None:
        return jsonify({"error": "ID должен быть положительным целым числом"}), 400

    game = find_game(game_id)
    if game is None:
        return jsonify({"error": "Игра не найдена"}), 404
    return jsonify(game), 200


@app.route('/games/<game_id>/reviews', methods=['GET'])
def get_reviews(game_id):
    game_id = parse_id(game_id)
    if game_id is None:
        return jsonify({"error": "ID должен быть положительным целым числом"}), 400

    game = find_game(game_id)
    if game is None:
        return jsonify({"error": "Игра не найдена"}), 404

    result = reviews.get(game_id, [])
    return jsonify({"game_id": game_id, "count": len(result), "reviews": result}), 200


@app.route('/platforms/<platform>/games', methods=['GET'])
def get_platform_games(platform):
    result = []
    for game in games:
        if game["platform"].lower() == platform.lower():
            result.append(game)
    return jsonify({"platform": platform, "count": len(result), "games": result}), 200


@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Маршрут не найден"}), 404


if __name__ == '__main__':
    app.run(port=3000, debug=True)
