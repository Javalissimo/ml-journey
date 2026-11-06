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