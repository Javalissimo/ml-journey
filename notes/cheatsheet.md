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


`*args` → tuple (порядок), `**kwargs` → dict;
```python
def convert_record(record: dict, mapping: dict, **defaults) -> tuple[dict, list]: 
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
Python видит присваивание total = 5 в функции → имя total локальное во всей функции → строка print(total) читает пустую локальную → UnboundLocalError.
Пример:
```python
total = 100
def f2():
    print(total)
    total = 5
```
```python
def add_item(item, items=[]):
    items.append(item)
    return items

print(add_item('a'))
print(add_item('b'))
```
при такой записи список создается когда питон читает функцию, и потом в этот список все добавляется. Правильно вот так:
```python
def add_item(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items
```


Рецепт скобок: [ ] даёт список, { : } словарь, { } множество.
ids = [o['id'] for o in orders if o['total'] > 1000]

Если от модели требуется "Да" или "Нет" то это бинарная классификация


## 06.11
```
Какой ответ ожидается	Тип задачи
Число	                регрессия (regression)
2 метки («да / нет»)	бинарная классификация (binary classification)
3 и больше меток	    многоклассовая классификация (multiclass classification)
Меток нет, ищем группы	кластеризация (clustering)
```


Агрегатные функции SQL 
```
SQL	                        Что делает	                             Как в Excel
COUNT(*)	                число строк	                             число строк в таблице
COUNT(столбец)	            число строк, где в столбце не NULL	     СЧЁТЗ
SUM(столбец)	            сумма	                                 СУММ
AVG(столбец)	            среднее	                                 СРЗНАЧ
MIN(столбец) / MAX(столбец)	минимум / максимум	                     МИН / МАКС
```

Порядок выполнения SQL
```
1. FROM       — взять таблицу
2. WHERE      — отобрать строки
3. GROUP BY   — сложить в стопки
4. HAVING     — отобрать стопки
5. SELECT     — посчитать и показать столбцы
6. ORDER BY   — отсортировать
7. LIMIT      — обрезать
```

WHERE фильтрует отдельные строки до их группировки
HAVING фильтрует уже сформированные группы после применения GROUP BY
COUNT(*) отличается от COUNT(city) тем, что он считает NULL
COUNT(*) даёт 40, COUNT(city) даёт 37, потому что у 3 клиентов city равен NULL

Поиск дубликатов делается связкой GROUP BY + HAVING: сгруппировать по полю и оставить группы больше одной строки.


SELECT email, COUNT(*) AS cnt
FROM customers
GROUP BY email
HAVING COUNT(*) > 1;

Чтобы убрать группу с NULL нужно добавить WHERE email IS NOT NULL

в WHERE мы пишем условие которое мы видим в одной строке
в HAVING мы пишем условие которое видно только у группы строк
```SQL
SELECT customer_id, count(status)   
FROM ORDERS
WHERE status = 'отменён' --смотрим по одной строке
GROUP BY CUSTOMER_ID 
HAVING count(status) > 1; --смотрим по группе
```


# 08.11

**GROUP BY по двум столбцам** — группа = каждая комбинация, которая реально есть в данных (не 8 × 3 = 24, а 17). Порядок столбцов в `GROUP BY` на группы не влияет; порядок строк гарантирует только `ORDER BY`.

**Псевдоним:** в `ORDER BY` можно везде (он после `SELECT`), в `HAVING` — только в SQLite (он до `SELECT`). Надёжно: `HAVING COUNT(*) > 3`.

**Топ-N:** смотри, что стоит сразу после границы `LIMIT` — при равных значениях база отрежет любые (у нас 4 клиента с 8 заказами).

**Средний чек ≠ AVG по строкам** (385 — средняя строка, 997.03 — средний чек). `* 1.0` — ДО деления, иначе дробь уже потеряна:

```sql
SELECT ROUND(SUM(qty * price) * 1.0 / COUNT(DISTINCT order_id), 2) AS avg_check
FROM order_items;   -- 997.03
```

**COALESCE** меняет только `NULL` и только в выводе (в таблице `NULL` остаётся); `'казань'` — не пропуск, остаётся своей группой. 

```sql
SELECT COALESCE(promo_code, 'без промокода') AS promo, COUNT(*) AS orders_count
FROM orders
GROUP BY COALESCE(promo_code, 'без промокода')
ORDER BY orders_count DESC;   -- 159 / 11 / 5 / 2 = 177
```


# 10.11

```python
def check(total, city=None):
    if total > 1000:
        if city == 'Казань':
            return 'крупный, Казань'
    else:
        print('мелкий заказ')
        return 'мелкий'

a = check(500)
b = check(1500, city='Москва')
c = check(1500, city='Казань')
print(a, b, c)
```
Вывод: 
```
мелкий заказ
мелкий None крупный, Казань
```
Eсли дергаем функцию то принт всегда срабатывает, если питон доходит до этой строчки. return хранится в переменной и сам не печатается. Печатается только с помощью print(). всегда внимательно смотреть на условия if. иногда пропускаю и понимаю код неправильно.


GROUP BY не создаёт группу для того, чего нет в строках.
Если у нас 16 товаров в таблице с товарами, и какой то товар ни разу не купили, то в выгрузке из таблицы с продажами его не будет и отчет будет не корректным. 


## 11.11

```python
def add_city(city, cities=[]):
    cities.append(city)
    return cities

x = add_city('Казань')
y = add_city('Москва')
z = add_city('Сочи', [])
print(x, y, z)
print(x is y, x is z)
```

x и y ссылаются на один объект в памяти, соответственно вывод будет одинаковый (2 раза ['Казань', 'Москва'])

При проверке среднего (AVG) нужно использовать здравый смысл. Среднее не может быть больше максимально значения диапазона.


## 12.11

import math отличается от from math import sqrt тем, что при import math sqrt вызывается через точку
```python
import math
print(math.sqrt(16))
```
А если использовать from math import sqrt, то можно вызывать sqrt напрямую
```python
from math import sqrt
print(sqrt(16))
```
```python
import math  
print(sqrt(16)) #такой импорт вызовет ошибку
```


Модуль — это .py-файл. import math даёт имя math (math.sqrt), from math import sqrt даёт голое sqrt.
Python ищет модули в папке ноутбука, в стандартной библиотеке и в пакетах запущенного Python (поэтому важно, чтобы ядро было из .venv).
Модуль импортируется один раз за сессию: поменял .py → Restart Kernel.
try / except ТипОшибки позволяет программе пережить ожидаемую ошибку. Тип бери из последней строки traceback.
Голый except: прячет опечатки и баги. Лови только то, что ожидаешь.