from flask import Flask, jsonify

app = Flask(__name__)
app.json.ensure_ascii = False

cities = [
    {"id": 1, "name": "Москва", "population": 13000000, "country": "Россия", "area": 2561},
    {"id": 2, "name": "Санкт-Петербург", "population": 5600000, "country": "Россия", "area": 1439},
    {"id": 3, "name": "Новосибирск", "population": 1600000, "country": "Россия", "area": 505},
    {"id": 4, "name": "Екатеринбург", "population": 1500000, "country": "Россия", "area": 1112},
    {"id": 5, "name": "Казань", "population": 1250000, "country": "Россия", "area": 425}
]


def parse_id(value):
    try:
        number = int(value)
    except ValueError:
        return None
    if number < 1:
        return None
    return number


def find_city(city_id):
    for city in cities:
        if city["id"] == city_id:
            return city
    return None


@app.route('/cities', methods=['GET'])
def get_cities():
    return jsonify({"count": len(cities), "cities": cities}), 200


@app.route('/cities/<city_id>', methods=['GET'])
def get_city(city_id):
    city_id = parse_id(city_id)
    if city_id is None:
        return jsonify({"error": "ID должен быть положительным целым числом"}), 400

    city = find_city(city_id)
    if city is None:
        return jsonify({"error": "Город не найден"}), 404
    return jsonify(city), 200


@app.route('/cities/<city_id>/area', methods=['GET'])
def get_city_area(city_id):
    city_id = parse_id(city_id)
    if city_id is None:
        return jsonify({"error": "ID должен быть положительным целым числом"}), 400

    city = find_city(city_id)
    if city is None:
        return jsonify({"error": "Город не найден"}), 404
    return jsonify({"city": city["name"], "area": city["area"], "unit": "км²"}), 200


@app.route('/countries/<country>/cities', methods=['GET'])
def get_country_cities(country):
    result = []
    for city in cities:
        if city["country"].lower() == country.lower():
            result.append(city)
    return jsonify({"country": country, "count": len(result), "cities": result}), 200


@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Маршрут не найден"}), 404


if __name__ == '__main__':
    app.run(port=3001, debug=True)
