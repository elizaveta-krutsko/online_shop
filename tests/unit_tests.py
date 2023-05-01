import unittest
from utils import get_password_hash, verify_password, create_tree


class TestPasswordHash(unittest.TestCase):
    def test_hardcode_hash(self):
        test_password = '123456@#Zxde'
        test_hash = get_password_hash(test_password)
        result_password = verify_password(test_password, test_hash)
        self.assertTrue(test_hash, result_password)


class TestCategoryTree(unittest.TestCase):
    def test_category_tree_result(self):
        test_categories = [
            {'_sa_instance_state': 0, 'parent_category_id': None, 'id': 1, 'name': 'milk', 'items': [1, 2, 3]},
            {'_sa_instance_state': 1, 'parent_category_id': None, 'id': 2, 'name': 'vegetables', 'items': []},
            {'_sa_instance_state': 2, 'parent_category_id': None, 'id': 3, 'name': 'fruits', 'items': []},
            {'_sa_instance_state': 3, 'parent_category_id': 2, 'id': 5, 'name': 'tomatos', 'items': []},
            {'_sa_instance_state': 4, 'parent_category_id': 2, 'id': 6, 'name': 'cucumbers'},
            {'_sa_instance_state': 5, 'parent_category_id': 2, 'id': 7, 'name': 'carrot'},
            {'_sa_instance_state': 6, 'parent_category_id': 3, 'id': 8, 'name': 'apples'},
            {'_sa_instance_state': 7, 'parent_category_id': 3, 'id': 9, 'name': 'oranges', 'items': []}
        ]
        test_result = [
         {'_sa_instance_state': 0,
          'id': 1,
          'items': [1, 2, 3],
          'name': 'milk',
          'parent_category_id': None},
         {'_sa_instance_state': 1,
          'id': 2,
          'items': [],
          'name': 'vegetables',
          'parent_category_id': None},
         {'_sa_instance_state': 2,
          'id': 3,
          'items': [],
          'name': 'fruits',
          'parent_category_id': None},
         {'_sa_instance_state': 3,
          'id': 5,
          'items': [],
          'name': 'tomatos',
          'parent_category_id': 2},
         {'_sa_instance_state': 4,
          'id': 6,
          'name': 'cucumbers',
          'parent_category_id': 2},
         {'_sa_instance_state': 5, 'id': 7, 'name': 'carrot', 'parent_category_id': 2},
         {'_sa_instance_state': 6, 'id': 8, 'name': 'apples', 'parent_category_id': 3},
         {'_sa_instance_state': 7,
          'id': 9,
          'items': [],
          'name': 'oranges',
          'parent_category_id': 3}
         ]
        self.assertEqual(test_categories, test_result)


if __name__ == '__main__':
    unittest.main()
