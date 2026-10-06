from flask import Flask, jsonify, request

app = Flask(__name__)
app.json.ensure_ascii = False
items = [
    {"id": 1, "name": "Товар 1", "price": 100, "quantity": 5},
    {"id": 2, "name": "Товар 2", "price": 200, "quantity": 3},
    {"id": 3, "name": "Товар 3", "price": 300, "quantity": 10}
]
next_id = 4


def find_item(item_id):
    for item in items:
        if item["id"] == item_id:
            return item
    return None


def validate_item(data):
    if not isinstance(data, dict):
        return "Нужно передать JSON-объект"

    name = data.get("name")
    if not isinstance(name, str) or not name.strip():
        return "name должен быть непустой строкой"

    price = data.get("price")
    if type(price) not in (int, float) or not 0 <= price < float("inf"):
        return "price должен быть неотрицательным числом"

    quantity = data.get("quantity")
    if type(quantity) is not int or quantity < 0:
        return "quantity должен быть целым неотрицательным числом"
    return None


@app.route('/items', methods=['GET'])
def get_items():
    return jsonify({"count": len(items), "items": items}), 200


@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = find_item(item_id)
    if item is None:
        return jsonify({"error": "Товар не найден"}), 404
    return jsonify(item), 200


@app.route('/items', methods=['POST'])
def create_item():
    global next_id
    data = request.get_json(silent=True)
    error = validate_item(data)
    if error is not None:
        return jsonify({"error": error}), 400

    item = {
        "id": next_id,
        "name": data["name"].strip(),
        "price": data["price"],
        "quantity": data["quantity"]
    }
    items.append(item)
    next_id += 1
    return jsonify(item), 201


@app.route('/items/<int:item_id>', methods=['PUT'])
def replace_item(item_id):
    item = find_item(item_id)
    if item is None:
        return jsonify({"error": "Товар не найден"}), 404

    data = request.get_json(silent=True)
    error = validate_item(data)
    if error is not None:
        return jsonify({"error": error}), 400

    item["name"] = data["name"].strip()
    item["price"] = data["price"]
    item["quantity"] = data["quantity"]
    return jsonify(item), 200


@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    item = find_item(item_id)
    if item is None:
        return jsonify({"error": "Товар не найден"}), 404
    items.remove(item)
    # В практическом примере методички возвращается 200 с JSON.
    return jsonify({"message": "Элемент удалён", "deleted": item}), 200


@app.errorhandler(404)
def route_not_found(error):
    return jsonify({"error": "Маршрут не найден"}), 404


if __name__ == "__main__":
    # Другой порт позволяет одновременно запустить API игр.
    app.run(port=3001, debug=True)
