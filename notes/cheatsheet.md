## 17.10 — повторение после теста

- Множество (set) выбрасывает дубликаты, оно неупорядоченное и его можно менять. Кортеж(tuple) хранит дубликаты и порядок и его нельзя менять.

- lambda записывается как lambda o: o["total"]
# то же самое, что:
def get_total(o):
    return o["total"]
Пример: sorted_order = sorted(orders, key=lambda o: o['city'])
Сортировка по городу и по сумме заказа(убывание) pprint.pprint(sorted(orders, key=lambda o: (o['city'], -o['total'])))



- comprehension: Взять поле из словаря: ids = [o['order_id'] for o in sorted_order]
собрать новый список словарей: [{'order_id': o['order_id']} for o in sorted_order]

- precision: Из тех кого модель отобрала КАКАЯ ДОЛЯ угадана (отобрала 40, из них ушло 20 -> 50%) 
 accuracy: Доля правильных ответов СРЕДИ ВСЕХ клиентов 
 accuracy = (угадала «уйдёт» + угадала «останется») / все клиенты = (20 + 930) / 1000 = 95 %.
⚠️ при редком классе «лентяй» тоже даёт 95 % → смотреть precision.

- SQL «не равно ни одному из»: 
WHERE city NOT IN ('Казань', 'казань')   
OR city IS NULL 

import sys                 # модуль с информацией о запущенном Python
print(sys.executable)      # путь к python.exe, который сейчас выполняет ноутбук

sorted создаёт новый список и возвращает его, а исходный не трогает. .sort() меняет исходный список на месте и возвращает None. Поэтому orders = orders.sort(...) затрёт список значением None

## 04.11 — функции


*args → tuple (порядок), **kwargs → dict;
```def convert_record(record: dict, mapping: dict, **defaults) -> tuple[dict, list]: 
    missing_fields = []
    new_record = {}
    for old_key, value in record.items():
        if old_key in mapping:
            new_key = mapping[old_key]
            new_record[new_key] = value
        else:
            missing_fields.append(old_key)
    
    for key, default_value in defaults.items():
        if key not in new_record:  # Данные клиента важнее чем новые 
            new_record[key] = default_value    
    
    return new_record, missing_fields
```
## 05.11
Python видит присваивание total = 5 в функции → имяtotal локальное во всей функции → строка print(total) читает пустую локальную → UnboundLocalError.
Пример:
```total = 100
def f2():
    print(total)
    total = 5
```
```def add_item(item, items=[]):
    items.append(item)
    return items

print(add_item('a'))
print(add_item('b'))
```
при такой записи список создается когда питон читает функцию, и потом в этот список все добавляется. Правильно вот так:
```def add_item(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items
```
Порядок выполнения в SQL FROM → WHERE → SELECT → ORDER BY → LIMIT

Рецепт скобок: [ ] даёт список, { : } словарь, { } множество.
ids = [o['id'] for o in orders if o['total'] > 1000]

Если от модели требуется "Да" или "Нет" то это бинарная классификация