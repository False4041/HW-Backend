import sqlite3

conn = sqlite3.connect('example.db')
cursor = conn.cursor()

print('1. CREATE TABLE и INSERT')
query = '''CREATE TABLE IF NOT EXISTS cities (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    population INTEGER,
    country TEXT DEFAULT 'Россия',
    area REAL
)'''
cursor.execute(query)
print(query)
cursor.execute('DELETE FROM cities')
cities = [
    (1, 'Москва', 13000000, 'Россия', 2561),
    (2, 'Санкт-Петербург', 5600000, 'Россия', 1439),
    (3, 'Новосибирск', 1600000, 'Россия', 505),
    (4, 'Екатеринбург', 1500000, 'Россия', 1112),
    (5, 'Казань', 1250000, 'Россия', 425),
    (6, 'Алматы', 2000000, 'Казахстан', 682)
]
query = 'INSERT INTO cities (id, name, population, country, area) VALUES (?, ?, ?, ?, ?)'
cursor.executemany(query, cities)
print(query)
print('Добавлено городов:', cursor.rowcount)

print('\n2. Все города')
query = 'SELECT * FROM cities'
cursor.execute(query)
print(query)
for row in cursor.fetchall():
    print(row)

print('\n3. Население больше 1.5 млн')
query = 'SELECT * FROM cities WHERE population > ?'
cursor.execute(query, (1500000,))
print(query, 'Параметр: 1500000')
for row in cursor.fetchall():
    print(row)

print('\n4. Сортировка по населению')
query = 'SELECT * FROM cities ORDER BY population DESC'
cursor.execute(query)
print(query)
for row in cursor.fetchall():
    print(row)

print('\n5. Первые три города')
query = 'SELECT * FROM cities LIMIT 3'
cursor.execute(query)
print(query)
for row in cursor.fetchall():
    print(row)

print('\n6. UPDATE и DELETE')
query = 'UPDATE cities SET population = ? WHERE id = ?'
cursor.execute(query, (13500000, 1))
print(query, 'Параметры: 13500000, 1')
print('Изменено городов:', cursor.rowcount)
query = 'DELETE FROM cities WHERE id = ?'
cursor.execute(query, (6,))
print(query, 'Параметр: 6')
print('Удалено городов:', cursor.rowcount)
cursor.execute('SELECT * FROM cities')
for row in cursor.fetchall():
    print(row)

print('\n7. Статистика')
query = '''SELECT COUNT(*), SUM(population), AVG(population),
       MAX(population), MIN(population) FROM cities'''
cursor.execute(query)
print(query)
print('Количество, сумма, среднее, максимум, минимум:')
print(cursor.fetchone())

print('\n8. Поиск по подстроке')
query = 'SELECT * FROM cities WHERE name LIKE ?'
cursor.execute(query, ('%бург%',))
print(query, 'Параметр: %бург%')
for row in cursor.fetchall():
    print(row)

conn.commit()
conn.close()
print('Изменения сохранены в example.db. Соединение закрыто.')
