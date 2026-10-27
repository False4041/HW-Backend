# Лабораторная работа №2
## HTTP-методы: обработка GET, POST, PUT, DELETE

**Студент:** Зорькин Арсений Станиславович  
**Группа:** ПИЖ-б-о-25-2(1)  
**Вариант:** 12  
**Уровень:** средний  
**Технология:** Python + Flask  
**Дата:** 06.10.2026

## Цель работы

Освоить получение, создание, обновление и удаление данных через HTTP. Реализовать API игр с хранением данных в памяти, проверкой входных данных, поиском, сортировкой и пагинацией.

## Теоретическое обоснование

CRUD объединяет четыре операции: создание, чтение, обновление и удаление. В этой работе им соответствуют методы POST, GET, PUT и DELETE. Маршрут Flask связывает метод и адрес запроса с функцией, которая формирует ответ.

Данные игры представлены словарём Python, а коллекция игр - списком словарей. Функция `jsonify()` формирует JSON-ответ. Код HTTP 200 означает успешное получение данных, 201 - создание ресурса, 204 - успешное действие без тела ответа, 400 - ошибку данных запроса, 404 - отсутствие ресурса.

Список хранится в памяти процесса. После остановки или автоматического перезапуска сервера изменения в нём теряются, и снова загружаются начальные данные из файла.

## Подготовка и запуск

Создан файл `app.py`, импортирован Flask и создан объект приложения.

![Создание приложения Flask](screenshots/app-created.png)

*Рисунок 1 - Начало работы с app.py*

Используются Python 3.14.2 и Flask 3.1.3. Команды PowerShell из папки проекта:

```powershell
python -m venv venv
.\venv\Scripts\python.exe -m pip install Flask==3.1.3
.\venv\Scripts\python.exe app.py
```

Сервер запускается на порту 3000. Параметр `debug=True` включает режим отладки и автоматический перезапуск при изменении сохранённого файла.

![Запуск Flask в терминале](screenshots/server-start.png)

*Рисунок 2 - Запуск сервера и успешный запрос GET /games*

В терминале видны сообщения `Debug mode: on`, `Restarting with stat` и ответ 200 для `GET /games`. Запрос корневого адреса `/` возвращает 404, поскольку такой маршрут не задан.

## Практический пример

Пример с товарами из методички адаптирован на Python и Flask. Исходный файл: [example.py](example.py). Сервер работает отдельно на порту 3001 и предоставляет GET, POST, PUT и DELETE для `/items`.

`app.py` - индивидуальное задание про игры. `example.py` - отдельный практический пример про товары, который требуется в отчёте. Он не заменяет основной файл. Эти два сервера запускаются независимо, поэтому у них разные порты. Остальные файлы содержат отчёт, запросы и проверки; их не нужно запускать как сервер.

```powershell
.\venv\Scripts\python.exe example.py
```

В примере DELETE возвращает 200 и данные удалённого товара. В индивидуальном задании используется 204 без тела ответа, как требует средний уровень. Запросы практического примера находятся в первой папке коллекции Postman. Скриншоты этого примера ещё не добавлены.

Код практического примера:

```python
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
```

## Индивидуальное задание

Для варианта 12 используется сущность «Игры». Поля базового уровня: `id`, `title`, `genre`. На среднем уровне добавлены `platform` и `rating`.

### Код сервера

[Файл app.py](app.py)

```python
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
```

![Код списка игр и обработчика GET](screenshots/games-code.png)

*Рисунок 3 - Начальные данные и обработчик GET /games в app.py*

### Получение списка игр

Обработчик `GET /games` возвращает количество записей и список игр. Начальные данные содержат Minecraft, Portal 2 и God of War.

Проверка в браузере:

```text
http://127.0.0.1:3000/games
```

![Список игр в браузере](screenshots/games-all.png)

*Рисунок 4 - JSON-ответ GET /games: count равен 3*

### Получение игры по ID

Маршрут `GET /games/<int:game_id>` принимает числовой ID и ищет игру в списке. При совпадении возвращается игра, при отсутствии записи - JSON с сообщением «Игра не найдена» и статусом 404.

![Код получения игры по ID](screenshots/games-by-id-code.png)

*Рисунок 5 - Обработчик получения игры по ID*

Проверены запросы `GET /games/2` и `GET /games/999`. Первый возвращает Portal 2 со статусом 200, второй - сообщение об отсутствии игры со статусом 404.

![Ответ с данными Portal 2](screenshots/game-found.png)

*Рисунок 6 - Получение игры с ID 2*

![Ответ для отсутствующей игры](screenshots/game-not-found.png)

*Рисунок 7 - Сообщение об отсутствии игры с ID 999*

Во втором ответе русские буквы записаны как последовательности `\uXXXX`. Это допустимое представление символов в JSON; сообщение означает «Игра не найдена».

### Проверка текстовых полей

Добавлена функция `validate_game(data)`. Она проверяет, что данные являются словарём, а поля `title`, `genre` и `platform` содержат непустые строки. Если обнаружена ошибка, функция возвращает её описание. Значение `None` означает, что эти проверки пройдены.

![Проверка текстовых полей игры](screenshots/validation-text-fields.png)

*Рисунок 8 - Проверка формата данных и текстовых полей*

### Проверка рейтинга

После проверки текстовых полей функция проверяет `rating`. Допускаются целые и дробные числа от 0 до 10. Строка с числом, логическое значение, отсутствующее поле и число вне диапазона возвращают сообщение об ошибке.

![Проверка рейтинга игры](screenshots/validation-rating.png)

*Рисунок 9 - Проверка типа и диапазона рейтинга*

Проверка функции на примерах подтвердила, что корректная игра с рейтингом 9.5 проходит, а неверный рейтинг, пропущенное текстовое поле и данные в виде списка отклоняются.

### Проверка функции в Python

Функция импортирована командой `from app import validate_game` в отдельном терминале Python. Для игры Hades с рейтингом 9.5 функция вернула `None`. После изменения рейтинга на 11 вернулось сообщение «Рейтинг должен быть числом от 0 до 10».

![Проверка validate_game в терминале Python](screenshots/validation-console.png)

*Рисунок 10 - Проверка корректных данных и рейтинга вне диапазона*

Затем рейтинг возвращён к значению 9.5, а название заменено строкой из пробелов. Функция вернула сообщение «Поле title должно быть непустой строкой».

![Проверка названия из пробелов](screenshots/validation-empty-title.png)

*Рисунок 11 - Отклонение пустого названия игры*

### Проверка данных POST-запроса

При первоначальной проверке обработчик `POST /games` читал JSON из тела запроса и вызывал `validate_game`. При ошибке возвращался JSON с её описанием и статусом 400. Корректные данные возвращались обратно со статусом 200 без записи в список игр. Далее обработчик дополнен созданием записи.

Проверены ответы работающего сервера: корректная игра получает статус 200, а рейтинг 11 - статус 400. Отдельно проверены пустое название, неверный тип рейтинга и некорректный JSON. Маршруты GET продолжают работать.

![Функция проверки данных и обработчик POST](screenshots/post-validation-code.png)

*Рисунок 12 - Чтение JSON, проверка данных и формирование ответа POST*

При отправке запроса из Postman без доступного обработчику JSON-объекта получен статус 400 Bad Request и сообщение «Нужно передать JSON-объект».

![Ответ POST при отсутствии JSON-объекта](screenshots/post-json-required.png)

*Рисунок 13 - Ответ 400 при неполучении JSON-объекта*

В Postman выбраны `Body`, `raw` и формат JSON. Переданы данные игры Hades с рейтингом 9.5. Сервер вернул эти данные со статусом 200 OK.

![Корректные данные POST в Postman](screenshots/post-validation-success.png)

*Рисунок 14 - Успешная проверка данных POST-запроса*

В том же запросе рейтинг заменён на 11. Сервер вернул статус 400 Bad Request и сообщение «Рейтинг должен быть числом от 0 до 10».

![Отклонение неверного рейтинга в Postman](screenshots/post-invalid-rating.png)

*Рисунок 15 - Проверка диапазона рейтинга через POST-запрос*

### Подготовка ID новой игры

После списка начальных игр добавлена переменная `next_id = 4`. Первые три номера уже заняты. Счётчик будет использоваться при создании новой игры и увеличиваться после добавления записи.

![Счётчик ID новой игры](screenshots/next-game-id.png)

*Рисунок 16 - Подготовка номера следующей игры*

### Создание новой игры

Обработчик `POST /games` дополнен созданием словаря игры. ID назначается из `next_id`, пробелы по краям текстовых полей удаляются. После проверки запись добавляется в `games`, счётчик увеличивается на один, а созданная игра возвращается со статусом 201 Created.

![Создание игры в обработчике POST](screenshots/post-create-code.png)

*Рисунок 17 - Добавление игры в список и ответ 201*

Проверка в отдельном экземпляре приложения подтвердила создание игры с ID 4, получение её через GET и увеличение количества записей до четырёх. Запрос с рейтингом 11 возвращает 400 без добавления записи. Следующий корректный запрос получает ID 5.

При отправке корректного JSON из Postman сервер вернул 201 Created и данные созданной игры Hades с ID 4.

![Создание Hades через Postman](screenshots/post-game-created.png)

*Рисунок 18 - Ответ 201 Created с ID созданной игры*

После создания выполнен `GET /games/4` в Postman. Сервер вернул 200 OK и данные Hades с ID 4, платформой PC и рейтингом 9.5.

![Получение созданной игры через GET](screenshots/get-created-game.png)

*Рисунок 19 - Получение игры после добавления через POST*

### Изменение и удаление

`PUT /games/<id>` полностью заменяет четыре поля игры: `title`, `genre`, `platform`, `rating`. ID сохраняется. Все поля обязательны. Некорректные данные дают 400 и не изменяют запись; отсутствие игры даёт 404. Успешное изменение возвращает 200 и обновлённую игру.

`DELETE /games/<id>` удаляет найденную игру и возвращает 204 No Content с пустым телом. При повторном удалении той же записи возвращается 404. Номера удалённых игр не используются повторно в течение запуска сервера.

### Поиск, сортировка и пагинация

| Запрос | Действие |
| --- | --- |
| `GET /games?search=mine` | Поиск подстроки в названии без учёта регистра |
| `GET /games?sort=rating&order=asc` | Сортировка рейтинга по возрастанию |
| `GET /games?sort=rating&order=desc` | Сортировка рейтинга по убыванию |
| `GET /games?page=2&limit=1` | Вторая страница по одной игре |
| `GET /games?search=o&sort=title&order=asc&page=2&limit=1` | Поиск, сортировка и пагинация вместе |

Разрешены поля сортировки `id`, `title`, `genre`, `platform`, `rating`. Порядок: `asc` или `desc`. Значения `page` и `limit` должны быть целыми числами больше нуля. Неверные параметры возвращают 400.

Сначала выполняется поиск, затем сортировка, затем выделяется страница. `count` содержит общее число совпадений до пагинации, `games` - записи текущей страницы. По умолчанию используются `sort=id`, `order=asc`, `page=1`, `limit=10`. Страница за пределами списка возвращает пустой массив и статус 200.

### Понятное объяснение новых частей

`request.args` получает параметры из адреса. Например, в `/games?search=mine` параметр `search` равен `mine`. `request.get_json(silent=True)` читает тело POST или PUT; если JSON отсутствует или испорчен, возвращается `None`, и проверка выдаёт 400.

Поиск написан обычным циклом: перебираем игры и добавляем подходящие в новый список `result`. `casefold()` приводит текст к одному регистру, поэтому `mine` и `MiNe` находят одну и ту же игру. Новый список нужен, чтобы сортировка ответа не меняла исходный порядок в `games`.

`sort_key()` выбирает значение поля для сравнения: например, рейтинг игры. `result.sort()` сортирует список по этому значению. `reverse=True` включает обратный порядок, то есть `desc`.

`int()` превращает строку параметра в целое число. `try` и `except ValueError` позволяют вернуть 400 для `page=abc`, а не завершить обработку с ошибкой сервера. Для страницы вычисляется начало `(page - 1) * limit`, затем срез `result[start:start + limit]` выбирает нужные записи. `count` остаётся общим числом найденных игр.

`find_game()` ищет игру по ID обычным циклом. Если игра не найдена, функция возвращает `None`. Обработчики GET, PUT и DELETE в этом случае отвечают 404.

`validate_game()` проверяет обязательные поля, их типы и рейтинг от 0 до 10. Одна проверка используется в POST и PUT. Проверка выполняется до изменения списка, поэтому ошибочный запрос не портит данные.

PUT записывает новые значения в четыре поля найденной игры. Поле `id` сохраняется. DELETE удаляет игру через `games.remove(game)` и возвращает `'', 204`: пустую строку и код успешного удаления без тела ответа.

`next_id` - счётчик для новых игр. POST берёт текущий номер, добавляет игру в список и увеличивает номер на один. `app.json.ensure_ascii = False` делает русские сообщения читаемыми в JSON.

### Проверки и материалы Postman

В Postman выполнен запрос `GET /games?search=mine`. Сервер вернул 200 OK, одну найденную игру Minecraft и `count: 1`.

![Поиск игры в Postman](screenshots/search-postman.png)

*Рисунок 20 - Поиск Minecraft по части названия, ответ 200 OK*

- [Коллекция Postman v2.1](Lab2.postman_collection.json): готовые запросы, тела JSON и проверки ответов.
- [Проверки API](tests/test_api.py): создание, изменение, удаление, валидация, поиск, сортировка и страницы.
- [Результаты автоматической проверки](TEST_RESULTS.md).
- [Полный список запросов и состояния скриншотов](SCREENSHOTS.md).

Перед запуском коллекции нужно перезапустить `app.py` и `example.py`, чтобы восстановить исходные данные. Коллекция выполняется по порядку, сохраняет ID созданных записей в переменные и удаляет созданные записи после проверок. Снимок поиска добавлен. Снимки PUT, DELETE, сортировки, пагинации, практического примера, Test Results и Collection Runner ещё предстоит добавить.

## Ответы на контрольные вопросы

### 1. В чём разница между PUT и PATCH?

PUT используется для полной замены данных ресурса, PATCH - для изменения отдельных полей. В среднем уровне этой работы нужен PUT.

### 2. Как реализовать поиск по коллекции?

Получить параметр `search` из `request.args` и выбрать игры, названия которых содержат переданную строку.

### 3. Как реализовать сортировку по полю?

Проверить, что указанное поле разрешено, затем отсортировать записи по его значению. Параметр `order` задаёт порядок: `asc` или `desc`.

### 4. Как работает пагинация?

Коллекция разбивается на страницы. Для страницы `page` с размером `limit` первый индекс равен `(page - 1) * limit`. В ответ попадают записи выбранной страницы.

### 5. Какой код возвращается при ошибке валидации?

HTTP 400 Bad Request. В JSON-ответе следует указать, какие данные переданы неверно.

## Вывод

Реализован API игр на Flask с хранением данных в памяти. Поддерживаются получение списка и отдельной игры, создание, полное изменение и удаление. Добавлены проверка входных данных, поиск по названию, сортировка и пагинация. Для ответов используются коды 200, 201, 204, 400 и 404.

Во время выполнения возникали ошибки с отступами, сохранением файла и запуском сервера. Проверки функции в Python и запросы Postman помогли найти причины. Данные исчезают при перезапуске, поскольку база данных в этой работе не используется.

## Источники

1. Лабораторная работа №2 «HTTP-методы: обработка GET, POST, PUT, DELETE»: средний уровень и вариант 12.
2. [Flask: Quickstart](https://flask.palletsprojects.com/en/stable/quickstart/).
3. [Postman: отправка запросов](https://learning.postman.com/docs/sending-requests/requests/).
4. Инструкция по настройке Postman для ЛР2: запросы, Test Results, экспорт коллекции и Collection Runner.
