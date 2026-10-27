from flask import Flask, jsonify, request

app = Flask(__name__)
# Показываем русские сообщения без кодов вида \u0418.
app.json.ensure_ascii = False

# Игры хранятся в памяти. При перезапуске изменения пропадают.
games = [
    {"id": 1, "title": "Minecraft", "genre": "Sandbox", "platform": "PC", "rating": 9.0},
    {"id": 2, "title": "Portal 2", "genre": "Puzzle", "platform": "PC", "rating": 9.5},
    {"id": 3, "title": "God of War", "genre": "Action", "platform": "PlayStation", "rating": 9.1}
]
next_id = 4


@app.route('/games', methods=['GET'])
def get_games():
    # Поиск по части названия без учёта регистра.
    search = request.args.get("search", "").strip().casefold()
    result = []
    for game in games:
        if search in game["title"].casefold():
            result.append(game)

    # Проверяем параметры сортировки.
    sort = request.args.get("sort", "id")
    order = request.args.get("order", "asc")
    if sort not in ("id", "title", "genre", "platform", "rating"):
        return jsonify({"error": "Неизвестное поле сортировки"}), 400
    if order not in ("asc", "desc"):
        return jsonify({"error": "Порядок должен быть asc или desc"}), 400

    # Номер страницы и её размер должны быть положительными числами.
    try:
        page = int(request.args.get("page", "1"))
        limit = int(request.args.get("limit", "10"))
    except ValueError:
        return jsonify({"error": "page и limit должны быть целыми числами"}), 400
    if page < 1 or limit < 1:
        return jsonify({"error": "page и limit должны быть больше нуля"}), 400

    def sort_key(game):
        value = game[sort]
        if isinstance(value, str):
            return value.casefold()
        return value

    result.sort(key=sort_key, reverse=(order == "desc"))
    count = len(result)
    # Например, page=2 и limit=1: начало страницы имеет индекс 1.
    start = (page - 1) * limit
    return jsonify({
        "count": count,
        "page": page,
        "limit": limit,
        "games": result[start:start + limit]
    }), 200


@app.route('/games/<int:game_id>', methods=['GET'])
def get_game(game_id):
    game = find_game(game_id)
    if game is None:
        return jsonify({"error": "Игра не найдена"}), 404
    return jsonify(game), 200


def find_game(game_id):
    for game in games:
        if game["id"] == game_id:
            return game
    return None


def validate_game(data):
    # Проверка общая для создания и полного обновления игры.
    if not isinstance(data, dict):
        return "Нужно передать JSON-объект"

    for field in ("title", "genre", "platform"):
        value = data.get(field)
        if not isinstance(value, str) or not value.strip():
            return f"Поле {field} должно быть непустой строкой"

    rating = data.get("rating")
    # True и False не считаем числовым рейтингом.
    if type(rating) not in (int, float) or not 0 <= rating <= 10:
        return "Рейтинг должен быть числом от 0 до 10"
    return None


@app.route('/games', methods=['POST'])
def create_game():
    global next_id
    # Если JSON не передан или испорчен, data будет None.
    data = request.get_json(silent=True)
    error = validate_game(data)

    if error is not None:
        return jsonify({"error": error}), 400

    game = {
        "id": next_id,
        "title": data["title"].strip(),
        "genre": data["genre"].strip(),
        "platform": data["platform"].strip(),
        "rating": data["rating"]
    }
    games.append(game)
    next_id += 1

    return jsonify(game), 201


@app.route('/games/<int:game_id>', methods=['PUT'])
def update_game(game_id):
    game = find_game(game_id)
    if game is None:
        return jsonify({"error": "Игра не найдена"}), 404

    data = request.get_json(silent=True)
    error = validate_game(data)
    if error is not None:
        return jsonify({"error": error}), 400

    # Меняем все четыре поля. ID остаётся прежним.
    game["title"] = data["title"].strip()
    game["genre"] = data["genre"].strip()
    game["platform"] = data["platform"].strip()
    game["rating"] = data["rating"]
    return jsonify(game), 200


@app.route('/games/<int:game_id>', methods=['DELETE'])
def delete_game(game_id):
    game = find_game(game_id)
    if game is None:
        return jsonify({"error": "Игра не найдена"}), 404
    games.remove(game)
    # Ответ 204 не должен содержать JSON или другой текст.
    return '', 204


@app.errorhandler(404)
def route_not_found(error):
    return jsonify({"error": "Маршрут не найден"}), 404


if __name__ == '__main__':
    app.run(port=3000, debug=True)
