from classes import Hub, Item


hub = Hub()
items_list = [Item(f'Some item{i}', f'Some desc{i}', 100 * i) for i in range(10)]
a_item = Item('Asics', 'sneakers', 200)

for el in items_list:
    hub.add_item(el)
hub.add_item(a_item)

A = [item for item in hub.get_items() if item.get_name().lower().startswith('a')]
MostValuable = hub.find_most_valuable(10)
Others = [item for item in hub.get_items() if item not in MostValuable]

# Не понял задание 'Выбросите все объекты с датой отправки раньше чем дата в hub, записав их в отдельный лист Outdated',
# с какой датой тут нужно было поработать?

