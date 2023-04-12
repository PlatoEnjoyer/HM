from datetime import datetime
import uuid


def singleton(cls):
    instances = {}

    def getinstance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)

        return instances[cls]

    return getinstance


@singleton
class Hub:

    def __init__(self):
        self._items = []
        self._date = datetime.now()

    def add_item(self, item):
        assert type(item) is Item, 'Добавлять можно лишь объекты типа Item'
        self._items.append(item)
        self._items[-1]._dispatch_time = datetime.now()

    def __getitem__(self, key):
        return self._items[key]

    def __repr__(self):
        if len(self._items) > 2:
            return str(self._items[:3])
        else:
            return str(self._items)

    def __str__(self):
        return f"На складе {len(self._items)} предметов, последнее обновление было сделано {self._date}"

    def __len__(self):
        return len(self._items)

    def find_by_id(self, id):
        for i, item in enumerate(self._items):
            if item._id == id:
                return i, item._name

        return -1, None

    def find_by_tags(self, tags):
        res = []
        for item in self._items:
            if item.is_tagged(tags):
                res.append(str(item))
        return res

    def rm_item(self, i):
        if type(i) is uuid.UUID:
            for item in self._items:
                if type(item) == Item and item._id == i:
                    self._items.remove(item)
                    break

        if type(i) is str:
            for item in self._items:
                if type(item) == Item and item._name == i:
                    self._items.remove(item)
                    break

    def drop_items(self, items):
        for i in items:
            self.rm_item(i)

    def clear(self):
        self._items = []

    def set_date(self):
        self._date = datetime.now()

    def get_date(self):
        return self._date

    def find_most_valuable(self, amount=1):
        return sorted(self._items[:amount], key=lambda i: i._cost, reverse=True)

    def find_by_date(self, first_date, second_date=None):
        if second_date:
            return [item for item in self._items if first_date <= item._dispatch_time <= second_date]

        else:
            return [item for item in self._items if item._dispatch_time <= first_date]

    def get_items(self):
        return self._items


class Item:

    def __init__(self, name, description, cost=50):
        self._id = uuid.uuid4()
        self._name = name
        self._description = description
        self._dispatch_time = datetime.now()
        self._tags = set()
        self._cost = cost

    def add_tags(self, tags):
        for el in tags:
            self._tags.add(el)

    def rm_tags(self, tags):
        for el in tags:
            self._tags.remove(tags)

    def __repr__(self):
        if not self._tags:
            return str(self._id)

        if len(self._tags) > 2:
            return str(self._tags[:3]) + '\n' + str(self._id)
        else:
            return str(self._tags) + '\n' + str(self._id)

    def __str__(self):
        return f"Предмет {self._name} был добавлен {self._dispatch_time}"

    def __len__(self):
        return len(self._tags)

    def is_tagged(self, tags):
        """
        :param tags: один тег или список тегов
        :return: True если tags полностью содержится в self._tags
        """
        if self._tags:
            if type(tags) in (tuple, list, set):
                tags = set(tags)
                return tags.issubset(self._tags)
            else:
                return tags in self._tags
        else:
            return False

    def set_cost(self, new_cost):
        self._cost = new_cost

    def get_cost(self):
        return self._cost

    def __lt__(self, other):
        return self._cost > other

    def copy(self):
        return Item(self._name, self._description, self._cost)

    def get_name(self):
        return self._name
