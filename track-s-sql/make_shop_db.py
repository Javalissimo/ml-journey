"""Создаёт учебную базу продаж data/shop.db для трека S (SQL).

Запуск из корня репозитория ml-journey:
    python track-s-sql/make_shop_db.py

Скрипт можно запускать сколько угодно раз: старая база удаляется
и создаётся заново с ТЕМИ ЖЕ данными (random.seed фиксирован).
Сама база лежит в data/ (папка в .gitignore), а в git хранится только этот скрипт.

Таблицы:
    customers   — клиенты (есть пропуски NULL в city и email)
    products    — товары
    orders      — заказы (promo_code почти всегда NULL)
    order_items — строки заказов: какой товар, сколько, по какой цене
    payments    — оплаты (у отменённых заказов оплаты нет, у некоторых доставленных — тоже)
"""

import random
import sqlite3
from datetime import date, timedelta
from pathlib import Path

SEED = 42
DB_PATH = Path(__file__).resolve().parent.parent / "data" / "shop.db"

SCHEMA = """
CREATE TABLE customers (
    customer_id   INTEGER PRIMARY KEY,
    full_name     TEXT    NOT NULL,
    city          TEXT,              -- может быть NULL
    email         TEXT,              -- может быть NULL
    segment       TEXT    NOT NULL,  -- 'розница' / 'опт' / 'VIP'
    registered_at TEXT    NOT NULL   -- дата 'YYYY-MM-DD'
);

CREATE TABLE products (
    product_id INTEGER PRIMARY KEY,
    name       TEXT    NOT NULL,
    category   TEXT,                 -- может быть NULL
    price      INTEGER NOT NULL      -- цена в рублях
);

CREATE TABLE orders (
    order_id    INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES customers(customer_id),
    order_date  TEXT    NOT NULL,    -- 'YYYY-MM-DD'
    status      TEXT    NOT NULL,    -- 'доставлен' / 'в пути' / 'отменён'
    promo_code  TEXT                 -- чаще всего NULL
);

CREATE TABLE order_items (
    order_id   INTEGER NOT NULL REFERENCES orders(order_id),
    product_id INTEGER NOT NULL REFERENCES products(product_id),
    qty        INTEGER NOT NULL,
    price      INTEGER NOT NULL,     -- цена на момент заказа
    PRIMARY KEY (order_id, product_id)
);

CREATE TABLE payments (
    payment_id INTEGER PRIMARY KEY,
    order_id   INTEGER NOT NULL REFERENCES orders(order_id),
    amount     INTEGER NOT NULL,
    paid_at    TEXT    NOT NULL,     -- 'YYYY-MM-DD'
    method     TEXT    NOT NULL      -- 'карта' / 'СБП' / 'наличные'
);
"""

MALE = [("Иванов", "Иван"), ("Петров", "Сергей"), ("Смирнов", "Алексей"), ("Кузнецов", "Дмитрий"),
        ("Попов", "Андрей"), ("Соколов", "Михаил"), ("Лебедев", "Никита"), ("Козлов", "Артём"),
        ("Новиков", "Павел"), ("Морозов", "Егор"), ("Волков", "Олег"), ("Зайцев", "Роман"),
        ("Павлов", "Максим"), ("Семёнов", "Кирилл"), ("Голубев", "Денис"), ("Виноградов", "Илья"),
        ("Богданов", "Антон"), ("Воробьёв", "Тимур"), ("Фёдоров", "Глеб"), ("Михайлов", "Юрий")]
FEMALE = [("Иванова", "Анна"), ("Петрова", "Мария"), ("Смирнова", "Елена"), ("Кузнецова", "Ольга"),
          ("Попова", "Наталья"), ("Соколова", "Ирина"), ("Лебедева", "Татьяна"), ("Козлова", "Дарья"),
          ("Новикова", "Ксения"), ("Морозова", "Полина"), ("Волкова", "Алина"), ("Зайцева", "Вера"),
          ("Павлова", "Софья"), ("Семёнова", "Юлия"), ("Голубева", "Светлана"), ("Виноградова", "Марина"),
          ("Богданова", "Екатерина"), ("Воробьёва", "Анастасия"), ("Фёдорова", "Людмила"), ("Михайлова", "Ника")]

CITIES = ["Москва", "Москва", "Москва", "Санкт-Петербург", "Санкт-Петербург",
          "Казань", "Сочи", "Новосибирск", "Екатеринбург"]

PRODUCTS = [
    ("Хлеб бородинский", "Хлеб", 65), ("Батон нарезной", "Хлеб", 55), ("Круассан", "Хлеб", 90),
    ("Молоко 3,2 %", "Молочка", 95), ("Кефир 1 %", "Молочка", 85), ("Сыр российский", "Молочка", 520),
    ("Творог 5 %", "Молочка", 180), ("Сок яблочный", "Напитки", 140), ("Вода 1,5 л", "Напитки", 60),
    ("Кофе молотый", "Напитки", 690), ("Гречка", "Бакалея", 110), ("Рис", "Бакалея", 120),
    ("Масло подсолнечное", "Бакалея", 160), ("Шоколад горький", "Сладости", 150),
    ("Печенье овсяное", None, 130),          # категория не заполнена
    ("Торт «Медовик»", "Сладости", 890),     # этот товар никто не покупал
]
NEVER_SOLD = "Торт «Медовик»"

PROMOS = ["OSEN10", "WELCOME", "VIP15"]


def rand_date(start: date, end: date) -> date:
    return start + timedelta(days=random.randint(0, (end - start).days))


def build(conn: sqlite3.Connection) -> None:
    conn.executescript(SCHEMA)

    # --- клиенты -----------------------------------------------------------
    people = random.sample(MALE, 20) + random.sample(FEMALE, 20)
    random.shuffle(people)
    customers = []
    for cid, (last, first) in enumerate(people, start=1):
        city = random.choice(CITIES)
        if cid in (7, 23, 31):
            city = None                        # пропуск: город не указан
        if cid == 12:
            city = "казань"                    # «грязное» значение, как в реальной выгрузке
        email = None if random.random() < 0.15 else f"client{cid:02d}@example.com"
        segment = random.choices(["розница", "опт", "VIP"], weights=[70, 20, 10])[0]
        reg = rand_date(date(2024, 1, 1), date(2026, 6, 30))
        customers.append((cid, f"{last} {first}", city, email, segment, reg.isoformat()))
    conn.executemany("INSERT INTO customers VALUES (?, ?, ?, ?, ?, ?)", customers)

    # --- товары ------------------------------------------------------------
    conn.executemany(
        "INSERT INTO products VALUES (?, ?, ?, ?)",
        [(pid, n, c, p) for pid, (n, c, p) in enumerate(PRODUCTS, start=1)],
    )
    sellable = [(pid, p) for pid, (n, _, p) in enumerate(PRODUCTS, start=1) if n != NEVER_SOLD]

    # --- заказы, строки заказов, оплаты ------------------------------------
    no_orders = {5, 18, 27, 36}                 # клиенты, которые ни разу не заказывали
    buyers = [c for c in customers if c[0] not in no_orders]
    orders, items, payments = [], [], []
    oid = 0
    for c in buyers:
        cid, reg = c[0], date.fromisoformat(c[5])
        n_orders = random.randint(6, 14) if c[4] == "VIP" else random.randint(1, 8)
        for _ in range(n_orders):
            oid += 1
            start = max(reg, date(2025, 1, 1))
            od = rand_date(start, date(2026, 9, 30))
            status = random.choices(["доставлен", "отменён"], weights=[90, 10])[0]
            if od >= date(2026, 9, 20) and status == "доставлен" and random.random() < 0.7:
                status = "в пути"                  # свежие заказы ещё едут
            promo = random.choice(PROMOS) if random.random() < 0.12 else None
            orders.append((oid, cid, od.isoformat(), status, promo))

            total = 0
            for pid, price in random.sample(sellable, random.randint(1, 4)):
                qty = random.randint(1, 5) if c[4] == "опт" else random.randint(1, 3)
                items.append((oid, pid, qty, price))
                total += qty * price

            unpaid = status == "в пути" or (status == "доставлен" and random.random() < 0.04)
            if status != "отменён" and not unpaid:
                paid = od + timedelta(days=random.randint(0, 2))
                method = random.choices(["карта", "СБП", "наличные"], weights=[55, 35, 10])[0]
                payments.append((len(payments) + 1, oid, total, paid.isoformat(), method))

    orders.sort(key=lambda o: o[2])            # нумерация заказов по дате
    renum = {old[0]: new for new, old in enumerate(orders, start=1)}
    orders = [(renum[o[0]], *o[1:]) for o in orders]
    items = [(renum[i[0]], *i[1:]) for i in items]
    payments = sorted(((renum[p[1]], *p[2:]) for p in payments), key=lambda p: p[2])
    payments = [(n, *p) for n, p in enumerate(payments, start=1)]

    conn.executemany("INSERT INTO orders VALUES (?, ?, ?, ?, ?)", orders)
    conn.executemany("INSERT INTO order_items VALUES (?, ?, ?, ?)", items)
    conn.executemany("INSERT INTO payments VALUES (?, ?, ?, ?, ?)", payments)
    conn.commit()


def main() -> None:
    random.seed(SEED)
    DB_PATH.parent.mkdir(exist_ok=True)
    DB_PATH.unlink(missing_ok=True)            # пересоздаём базу с нуля
    with sqlite3.connect(DB_PATH) as conn:
        build(conn)
        print(f"База создана: {DB_PATH}")
        for table in ["customers", "products", "orders", "order_items", "payments"]:
            n = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
            print(f"  {table:<12} {n:>4} строк")
    conn.close()


if __name__ == "__main__":
    main()
