SELECT COUNT(*) AS total_rows,
       COUNT(city) AS with_city
FROM customers;

--Запрос вернёт одну строку с двумя числами, сколько бы строк ни было в таблице.

--Главное правило: все функции, кроме COUNT(*), пропускают NULL.

SELECT city, COUNT(*) AS clients
FROM customers
GROUP BY city;

--Как это выглядит на маленьком примере:

/* Заказы (строки)		Результат
Казань, 1200	→ стопка «Казань» (2 строки)	Казань, 2
Москва, 450	→ стопка «Москва» (1 строка)	Москва, 1
Казань, 3100 */

SELECT city, COUNT(*) AS clients
   FROM customers
   WHERE segment = 'розница'
   GROUP BY city;

/* Ловушка SQLite. Если написать SELECT city, email, COUNT(*) ... GROUP BY city, 
SQLite не выдаст ошибку. Он молча покажет случайный email из стопки. 
В других СУБД (PostgreSQL и т. д.) будет ошибка. Поэтому правило 1 нужно соблюдать самому. */

SELECT city, COUNT(*) AS clients
FROM customers
--WHERE COUNT(*) >= 5      -- ❌ ошибка
GROUP BY city;

--Он падает: на этапе WHERE стопок ещё нет, значит, и COUNT(*) по стопке считать нечего. Для фильтра по готовым группам есть HAVING:


SELECT city, COUNT(*) AS clients
FROM customers
GROUP BY city
HAVING COUNT(*) >= 5;

/* --В HAVING пиши само выражение COUNT(*), а не псевдоним.

	WHERE	HAVING
 Что фильтрует	строки	группы
Когда работает	до GROUP BY	после GROUP BY
Можно ли агрегат	нет	да */ 


--COUNT(DISTINCT столбец) считает количество разных значений. NULL не считается, как и в любом COUNT(столбец).


SELECT COUNT(*) AS rows_cnt,
       COUNT(DISTINCT city) AS cities_cnt
FROM customers;

--Поиск дубликатов делается связкой GROUP BY + HAVING: сгруппировать по полю и оставить группы больше одной строки.


SELECT email, COUNT(*) AS cnt
FROM customers
GROUP BY email
HAVING COUNT(*) > 1;

/* ⚠️ Ловушка: клиенты без email (у нас их 5) образуют свою группу NULL. 
Она попадёт в результат с cnt = 5, хотя это не дубликаты, а пустые значения. 
Чтобы их убрать, добавь WHERE email IS NOT NULL. Он выполнится до группировки. */

SELECT segment, count(*) AS clients_count  -- 07.11 тренировка
FROM CUSTOMERS 
GROUP BY segment

SELECT customer_id, count(status)   -- 07.11 тренировка
FROM ORDERS
WHERE status = 'отменён'
GROUP BY CUSTOMER_ID 
HAVING count(status) > 1;

-- 08.11 S.2 ч.2
-- шаг 5: группировка по двум столбцам (17 строк, сумма 40)
SELECT city, segment, COUNT(*) AS customers_count
FROM customers
GROUP BY city, segment
ORDER BY city, segment;

-- заказы по годам и статусам (5 строк, сумма 177)
SELECT SUBSTR(order_date, 1, 4) AS order_year, status, COUNT(*) AS orders_count
FROM orders
GROUP BY SUBSTR(order_date, 1, 4), status
ORDER BY order_year, status;

-- шаг 6: топ клиентов по числу заказов (13 -> 11, затем 4 клиента по 8)
SELECT customer_id, COUNT(*) AS orders_count
FROM orders
GROUP BY customer_id
ORDER BY orders_count DESC
LIMIT 6;

-- топ-3 заказа по сумме: 83 / 156 / 117
SELECT order_id, SUM(qty * price) AS order_total
FROM order_items
GROUP BY order_id
ORDER BY order_total DESC
LIMIT 3;

-- шаг 7: строки / выручка / средняя строка: 458 / 176475 / 385.3
SELECT COUNT(*) AS lines_count, SUM(qty * price) AS revenue, AVG(qty * price) AS avg_line
FROM order_items;

-- средний чек: 997 (целочисленное деление) и 997.03
SELECT
    SUM(qty * price) / COUNT(DISTINCT order_id) AS avg_check_int,
    ROUND(SUM(qty * price) * 1.0 / COUNT(DISTINCT order_id), 2) AS avg_check
FROM order_items;

-- шаг 8: COALESCE (4 строки, сумма 177)
SELECT COALESCE(promo_code, 'без промокода') AS promo, COUNT(*) AS orders_count
FROM orders
GROUP BY COALESCE(promo_code, 'без промокода')
ORDER BY orders_count DESC;

-- 'не указан' — 3, 'казань' — отдельная группа (1)
SELECT COALESCE(city, 'не указан') AS city_clean, COUNT(*) AS customers_count
FROM customers
GROUP BY COALESCE(city, 'не указан')
ORDER BY customers_count DESC;


-- 10.11

SELECT
	METHOD,
	count(*) AS payments_count, --Число оплат
	sum(amount) AS total_amount, --сумма
	round(avg(amount), 2) AS avg_payment --средний платеж
FROM
	PAYMENTS P
GROUP BY
	METHOD
ORDER BY
	TOTAL_AMOUNT DESC

SELECT  --средний чек по каждому способу оплаты
    method,
    count(*) AS total_count,
    SUM(amount) * 1.0 / COUNT(DISTINCT order_id)  AS avg_check
FROM payments
GROUP BY METHOD
HAVING TOTAL_COUNT >20
ORDER BY avg_check DESC