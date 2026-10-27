import importlib.util
import unittest
from pathlib import Path


class GamesTests(unittest.TestCase):
    def setUp(self):
        path = Path(__file__).resolve().parents[1] / "app.py"
        spec = importlib.util.spec_from_file_location("games_test_app", path)
        self.module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.module)
        self.client = self.module.app.test_client()
        self.game = {"title": "Hades", "genre": "Roguelike", "platform": "PC", "rating": 9.5}

    def test_get_list_and_id(self):
        self.assertEqual(self.client.get('/games').json['count'], 3)
        self.assertEqual(self.client.get('/games/2').json['title'], 'Portal 2')
        for url in ['/games/999', '/games/abc', '/missing']:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 404)
            self.assertIn('error', response.json)

    def test_create_and_read(self):
        response = self.client.post('/games', json={**self.game, 'title': ' Hades '})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json, {'id': 4, **self.game})
        self.assertEqual(self.client.get('/games/4').json, response.json)
        self.assertEqual(self.client.get('/games').json['count'], 4)

    def test_validation_does_not_consume_id(self):
        for field in self.game:
            data = self.game.copy()
            del data[field]
            with self.subTest(missing=field):
                self.assertEqual(self.client.post('/games', json=data).status_code, 400)
        for rating in [-1, 11, '9.5', None, True, float('nan'), float('inf')]:
            with self.subTest(rating=rating):
                self.assertEqual(self.client.post('/games', json={**self.game, 'rating': rating}).status_code, 400)
        for field in ['title', 'genre', 'platform']:
            for value in ['   ', 42, None]:
                self.assertEqual(self.client.post('/games', json={**self.game, field: value}).status_code, 400)
        self.assertEqual(self.client.get('/games').json['count'], 3)
        self.assertEqual(self.client.post('/games', json=self.game).json['id'], 4)

    def test_malformed_json(self):
        for body in ['{broken', '[]', 'null', '42']:
            response = self.client.post('/games', data=body, content_type='application/json')
            self.assertEqual(response.status_code, 400)
        self.assertEqual(self.client.post('/games').status_code, 400)

    def test_rating_boundaries(self):
        for value in [0, 10, 9.5]:
            self.assertEqual(self.client.post('/games', json={**self.game, 'rating': value}).status_code, 201)

    def test_put_replaces_fields_and_preserves_id(self):
        response = self.client.put('/games/2', json=self.game)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'id': 2, **self.game})
        self.assertEqual(self.client.get('/games/2').json, response.json)
        self.assertEqual(self.client.put('/games/2', json=self.game).json, response.json)
        self.assertEqual(self.client.get('/games').json['count'], 3)

    def test_invalid_put_keeps_original(self):
        before = self.client.get('/games/2').json
        for data in [{'rating': 8}, {**self.game, 'rating': 11}, {**self.game, 'title': ''}]:
            self.assertEqual(self.client.put('/games/2', json=data).status_code, 400)
            self.assertEqual(self.client.get('/games/2').json, before)
        response = self.client.put('/games/2', data='{broken', content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(self.client.get('/games/2').json, before)
        self.assertEqual(self.client.put('/games/999', json=self.game).status_code, 404)

    def test_delete_has_no_body_and_id_is_not_reused(self):
        self.client.post('/games', json=self.game)
        response = self.client.delete('/games/4')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.data, b'')
        self.assertEqual(self.client.get('/games/4').status_code, 404)
        self.assertEqual(self.client.delete('/games/4').status_code, 404)
        self.assertEqual(self.client.get('/games').json['count'], 3)
        self.assertEqual(self.client.post('/games', json=self.game).json['id'], 5)

    def test_search_is_case_insensitive(self):
        response = self.client.get('/games?search=MiNe')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['count'], 1)
        self.assertEqual(response.json['games'][0]['id'], 1)
        self.assertEqual(self.client.get('/games?search=absent').json['games'], [])

    def test_sorting_does_not_change_storage(self):
        for order, ids in [('asc', [1, 3, 2]), ('desc', [2, 3, 1])]:
            data = self.client.get('/games?sort=rating&order=' + order).json
            self.assertEqual([game['id'] for game in data['games']], ids)
        for field in ['id', 'title', 'genre', 'platform', 'rating']:
            self.assertEqual(self.client.get('/games?sort=' + field).status_code, 200)
        self.assertEqual([g['id'] for g in self.client.get('/games').json['games']], [1, 2, 3])

    def test_pagination_and_combined_query(self):
        data = self.client.get('/games?page=2&limit=1').json
        self.assertEqual(data, {'count': 3, 'page': 2, 'limit': 1, 'games': [self.client.get('/games/2').json]})
        data = self.client.get('/games?search=o&sort=title&order=asc&page=2&limit=1').json
        self.assertEqual(data['count'], 2)
        self.assertEqual(data['games'][0]['title'], 'Portal 2')
        self.assertEqual(self.client.get('/games?page=99&limit=1').json['games'], [])

    def test_invalid_query(self):
        for query in ['sort=unknown', 'order=wrong', 'page=0', 'page=-1', 'limit=0', 'limit=-1', 'page=abc', 'limit=1.5']:
            with self.subTest(query=query):
                response = self.client.get('/games?' + query)
                self.assertEqual(response.status_code, 400)
                self.assertIn('error', response.json)


if __name__ == '__main__':
    unittest.main(verbosity=2)
