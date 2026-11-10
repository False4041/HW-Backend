import sqlite3

conn = sqlite3.connect('lab4.db')
cursor = conn.cursor()

print('1. CREATE TABLE')
query = '''CREATE TABLE IF NOT EXISTS games (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    genre TEXT NOT NULL,
    rating REAL
)'''
cursor.execute(query)
print(query)
cursor.execute('DELETE FROM games')
print('Таблица games готова, прежние учебные данные очищены.')

print('\n2. INSERT')
games = [
    (1, 'Minecraft', 'Sandbox', 9.0),
    (2, 'Portal 2', 'Puzzle', 9.5),
    (3, 'God of War', 'Action', 9.1),
    (4, 'Hades', 'Roguelike', 9.5),
    (5, 'Hollow Knight', 'Metroidvania', 9.0)
]
query = 'INSERT INTO games (id, title, genre, rating) VALUES (?, ?, ?, ?)'
cursor.executemany(query, games)
print(query)
for game in games:
    print(game)
print('Добавлено записей:', cursor.rowcount)

print('\n3. SELECT *')
query = 'SELECT * FROM games'
cursor.execute(query)
print(query)
for row in cursor.fetchall():
    print(row)

print('\n4. WHERE')
query = 'SELECT * FROM games WHERE rating >= ?'
cursor.execute(query, (9.2,))
print(query, 'Параметр: 9.2')
for row in cursor.fetchall():
    print(row)

print('\n5. UPDATE')
query = 'UPDATE games SET rating = ? WHERE id = ?'
cursor.execute(query, (9.2, 1))
print(query, 'Параметры: 9.2, 1')
print('Изменено записей:', cursor.rowcount)
cursor.execute('SELECT * FROM games WHERE id = ?', (1,))
print(cursor.fetchone())

print('\n6. DELETE')
query = 'DELETE FROM games WHERE id = ?'
cursor.execute(query, (5,))
print(query, 'Параметр: 5')
print('Удалено записей:', cursor.rowcount)
cursor.execute('SELECT * FROM games')
for row in cursor.fetchall():
    print(row)

conn.commit()
conn.close()
print('Изменения сохранены в lab4.db. Соединение закрыто.')
