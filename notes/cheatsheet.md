## 17.10 — повторение после теста

- Множество (set) выбрасывает дубликаты, оно неупорядочнное и его можно менять. Кортеж(tuple) Хранит дубликаты и порядок и его нельзя менять.

- lambda записывается как lambda o: o["total"]
# то же самое, что:
def get_total(o):
    return o["total"]
Пример: sorted_order = sorted(orders, key=lambda o: o['city'])

- comprehension: Взять поле из словаря: ids = [o['order_id'] for o in sorted_order]
взять ключ и значение: [{'order_id': o['order_id']} for o in sorted_order]

- precision: Из тех кого модель отобрала КАКАЯ ДОЛЯ угадана (отобрала 20, ушло 40 -> 50%) 
 accuracy: Доля правильных ответов СРЕДИ ВСЕХ клиентов (тут нужно научиться считать)
 accuracy = (угадала «уйдёт» + угадала «останется») / все клиенты = (20 + 930) / 1000 = 95 %.
⚠️ при редком классе «лентяй» тоже даёт 95 % → смотреть precision.

- SQL «не равно ни одному из»: 
WHERE city NOT IN ('Казань', 'казань')   
OR city IS NULL 

import sys                 # модуль с информацией о запущенном Python
print(sys.executable)      # путь к python.exe, который сейчас выполняет ноутбук