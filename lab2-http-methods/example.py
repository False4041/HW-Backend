from flask import Flask, jsonify, request, abort
from werkzeug.exceptions import HTTPException

app = Flask(__name__)
app.json.ensure_ascii = False
items = [
    {"id": 1, "name": "Товар 1", "price": 100, "quantity": 5},
    {"id": 2, "name": "Товар 2", "price": 200, "quantity": 3},
    {"id": 3, "name": "Товар 3", "price": 300, "quantity": 10}
]
next_id = 4


@app.errorhandler(HTTPException)
def http_error(error):
    response = error.get_response()
    response.data = app.json.dumps({"error": error.description})
    response.content_type = "application/json"
    return response


def find_item(item_id):
    for item in items:
        if item["id"] == item_id:
            return item
    abort(404, description="Товар не найден")


def read_item():
    data = request.get_json(silent=True)
    if not isinstance(data, dict) or not {"name", "price", "quantity"} <= data.keys():
        abort(400, description="Нужны поля name, price, quantity")
    if not isinstance(data["name"], str) or not data["name"].strip():
        abort(400, description="name должен быть непустой строкой")
    if type(data["price"]) not in (int, float) or not 0 <= data["price"] < float('inf'):
        abort(400, description="price должен быть неотрицательным числом")
    if type(data["quantity"]) is not int or data["quantity"] < 0:
        abort(400, description="quantity должен быть целым неотрицательным числом")
    return {key: data[key] for key in ("name", "price", "quantity")}


@app.get("/items")
def get_items():
    return jsonify({"count": len(items), "items": items})


@app.get("/items/<int:item_id>")
def get_item(item_id):
    return jsonify(find_item(item_id))


@app.post("/items")
def create_item():
    global next_id
    data = read_item()
    item = {"id": next_id, **data}
    next_id += 1
    items.append(item)
    return jsonify(item), 201


@app.put("/items/<int:item_id>")
def replace_item(item_id):
    item = find_item(item_id)
    data = read_item()
    item.clear()
    item.update({"id": item_id, **data})
    return jsonify(item)


@app.delete("/items/<int:item_id>")
def delete_item(item_id):
    item = find_item(item_id)
    items.remove(item)
    return jsonify({"message": "Элемент удалён", "deleted": item})


if __name__ == "__main__":
    app.run(port=3001, debug=True)
