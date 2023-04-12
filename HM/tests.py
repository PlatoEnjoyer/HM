import datetime
import unittest
from classes import Hub, Item


def fill_for_test():
    h = Hub()
    i0 = Item('some_item_0', 'some_desc', 100)
    i1 = Item('some_item_1', 'some_desc', 300)
    h.add_item(i0)
    h.add_item(i1)

    return h, i0, i1


class TestHub(unittest.TestCase):
    def test_hub_singleton(self):
        """
        Проверка того что hub - синглтон
        """
        self.assertTrue(Hub() is Hub())

    def test_len(self):
        """
        Проверка изменения значения len() после добавления предметов
        """
        h = Hub()
        pre_len = len(h._items)
        for i in range(5):
            h.add_item(Item(str(i), str(i)))
        self.assertEqual(len(h) - pre_len, 5)

    def test_get_index(self):
        """
        Проверка взятия элемента _items по индексу
        """
        h = Hub()
        h_element = h._items[0]
        self.assertEqual(h[0], h_element)

    def test_find_by_id(self):
        """
        Проверка поиска итема по id
        """
        h = Hub()
        i = Item('some_item', 'some_disc')
        h.add_item(i)
        fake_id = 1
        self.assertEqual(h.find_by_id(i._id), (len(h._items) - 1, i._name))
        self.assertEqual(h.find_by_id(fake_id), (-1, None))

    def test_rm_item(self):
        h, i0, i1 = fill_for_test()

        h.rm_item(i1._id)  # Проверка удаления по id
        h.rm_item(i0._name)  # Проверка удаления по name

        self.assertTrue((i0, i1) not in h._items)

    def test_drop_items(self):
        h, i0, i1 = fill_for_test()

        h.drop_items([i0._id, i1._name])
        self.assertTrue((i0, i1) not in h._items)

    def test_clear(self):
        h, i0, i1 = fill_for_test()
        h.clear()
        self.assertTrue(not h._items)

    def test_find_most_valuable(self):
        h, i0, i1 = fill_for_test()
        res = h.find_most_valuable(2)
        self.assertTrue(res[0]._cost > res[1]._cost)

    def test_find_by_date(self):
        h, i0, i1 = fill_for_test()
        i0._dispatch_time = datetime.datetime(2025, 12, 10)
        query = h.find_by_date(datetime.datetime(2020, 12, 10), datetime.datetime(2024, 12, 10))  # Проверка двух
        # параметров
        self.assertTrue(i1 in query and i0 not in query)
        query = h.find_by_date(datetime.datetime(2023, 12, 10))  # Проверка одного параметра
        self.assertTrue(i1 in query)


class TestItem(unittest.TestCase):
    def test_item_id(self):
        """
        Проверка уникальности id у класса Item
        """
        ids = []
        for i in range(10):
            item = Item('some_name', 'some_desc')
            ids.append(item._id)

        self.assertTrue(len(ids) == len(set(ids)))

    def test_len(self):
        """
        Проверка изменения значения len() после добавления тэгов
        """
        item = Item('some_name', 'some_desc')
        self.assertEqual(len(item), 0)
        for i in range(5):
            item.add_tags([f'SomeTag{i}'])
        self.assertEqual(len(item), 5)

    def test_equal_tags(self):
        """
        Проверка уникальности значений атрибута _tags
        """
        item = Item('some_name', 'some_desc')
        for i in range(3):
            item.add_tags(['SameTag'])
        self.assertEqual(len(item), 1)

    def test_is_tagged(self):
        i1 = Item('some_item', 'some_desc')
        self.assertFalse(i1.is_tagged(['x', 'y']))
        i1.add_tags('x')
        self.assertFalse(i1.is_tagged(['x', 'y']))
        i1.add_tags('y')
        self.assertTrue(i1.is_tagged(['x', 'y']))
        self.assertTrue(i1.is_tagged('x'))  # проверка кейса, в котором на вход передали строку

    def test_copy(self):
        i1 = Item('some_item', 'some_desc')
        i1_copy = i1.copy()
        self.assertEqual((i1._name, i1._description, i1._cost), (i1_copy._name, i1_copy._description, i1_copy._cost))
        self.assertNotEqual(i1._id, i1_copy._id)


if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
