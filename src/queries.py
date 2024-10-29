import sqlite3
from utils import get_db_path, get_start_and_end_dates


def read_query(query):
    conn = sqlite3.connect(get_db_path())
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results


def get_form1_table1_query(month_number, year):
    start_date_str, end_date_str = get_start_and_end_dates(month_number, year)

    # SQL query with the correct date range
    query = f"""
WITH product_list AS (
    SELECT DISTINCT category_id FROM products
),
inventory_data AS (
   SELECT
   		p.category_id,
   		COALESCE(i.previous_existence, 0) AS previous_existence,
        COALESCE(i.bought, 0) AS bought,
        COALESCE(i.previous_existence, 0) + COALESCE(i.bought, 0) AS addings,
        COALESCE(i.consumed, 0) AS consumed,
        COALESCE(i.previous_existence, 0) + COALESCE(i.bought, 0) - COALESCE(i.consumed, 0) AS actual_existence
    FROM product_list p
    LEFT JOIN (
        SELECT i.product_id, latest.category_id, i.previous_existence, i.bought, i.consumed, i.date
        FROM inventory i
            INNER JOIN (
                SELECT i.product_id, p.category_id, MAX(i.date) AS max_date
                FROM inventory i
                LEFT JOIN products p ON i.product_id = p.id
                WHERE i.date >= '{start_date_str}' AND i.date < '{end_date_str}'
                GROUP BY i.product_id, p.category_id
            ) latest ON i.product_id = latest.product_id AND i.date = latest.max_date
        ) i ON p.category_id = i.category_id
    )
    SELECT 
        category_id,
        SUM(previous_existence) AS previous_existence,
        SUM(bought) AS bought,
        SUM(addings) AS addings,
        SUM(consumed) AS consumed,
        SUM(actual_existence) AS actual_existence
    FROM 
        inventory_data
    GROUP BY 
    category_id;
    """
    return query


def get_form1_table2_query(month_number, year):
    start_date_str, end_date_str = get_start_and_end_dates(month_number, year)

    # SQL query with the correct date range
    query = f"""
SELECT 
    o.invoice,
    strftime('%d', o.date) || '-' ||
    substr('JanFebMarAprMayJunJulAugSepOctNovDec', (strftime('%m', o.date) - 1) * 3 + 1, 3) || '-' ||
    substr(strftime('%Y', o.date), 3, 2) AS formatted_date,
    s.name,
    sp.permit,
    SUM(CASE WHEN oc.category_id = 1 THEN oc.item_count ELSE 0 END) AS count_category_1,
    SUM(CASE WHEN oc.category_id = 2 THEN oc.item_count ELSE 0 END) AS count_category_2,
    SUM(CASE WHEN oc.category_id = 3 THEN oc.item_count ELSE 0 END) AS count_category_3,
    SUM(CASE WHEN oc.category_id = 4 THEN oc.item_count ELSE 0 END) AS count_category_4,
    SUM(CASE WHEN oc.category_id = 5 THEN oc.item_count ELSE 0 END) AS count_category_5
FROM orders o
INNER JOIN suppliers s ON o.supplier_id = s.id
INNER JOIN supplier_permits sp ON o.supplier_id = sp.supplier_id
INNER JOIN (
    SELECT 
        oi.order_id,
        p.category_id,
        COUNT(*) AS item_count
    FROM order_items oi
    JOIN products p ON oi.product_id = p.id
    GROUP BY oi.order_id, p.category_id 
) oc ON o.id = oc.order_id
WHERE o.date >= '{start_date_str}'
      AND o.date < '{end_date_str}'
      AND o.status = 'completed'
GROUP BY o.invoice, o.date, s.name, sp.permit
ORDER BY o.invoice;

    """
    return query


def get_form1_table1_query_old(month_number, year):
    start_date_str, end_date_str = get_start_and_end_dates(month_number, year)

    # SQL query with the correct date range
    query = f"""
    WITH products_list AS (
        SELECT 1 AS product_id
        UNION ALL
        SELECT 2
        UNION ALL
        SELECT 3
        UNION ALL
        SELECT 4
        UNION ALL
        SELECT 5
    )
    SELECT
        p.product_id,
        COALESCE(i.previous_existence, 0) AS previous_existence,
        COALESCE(i.bought, 0) AS bought,
        COALESCE(i.previous_existence, 0) + COALESCE(i.bought, 0) AS addings,
        COALESCE(i.consumed, 0) AS consumed,
        COALESCE(i.previous_existence, 0) + COALESCE(i.bought, 0) - COALESCE(i.consumed, 0) AS actual_existence
    FROM products_list p
    LEFT JOIN (
        SELECT i.product_id, i.previous_existence, i.bought, i.consumed, i.date
        FROM inventory i
        INNER JOIN (
            SELECT product_id, MAX(date) AS max_date
            FROM inventory
            WHERE date >= '{start_date_str}' AND date < '{end_date_str}'
            GROUP BY product_id
        ) latest ON i.product_id = latest.product_id AND i.date = latest.max_date
    ) i ON p.product_id = i.product_id
    ORDER BY p.product_id;
    """
    return query


def get_form2_table1_part1_query(year):

    query = f"""
    SELECT 
        pc.id,
        IFNULL(aq.authorized_quantity, 0) AS annual_authorized_quantity
        ,IFNULL(SUM(m.modification), 0) AS total_modifications
        --,IFNULL(aq.authorized_quantity,0) + IFNULL(SUM(m.modification),0)
    FROM product_categories pc
    LEFT JOIN authorized_buying_quantities aq
        ON pc.id = aq.category_id AND aq."year" = '{year}'
    LEFT JOIN authorized_quantity_modifications m
        ON pc.id = m.category_id AND strftime('%Y', m.date) = aq.YEAR
    GROUP BY pc.id;
    """
    return query


def get_form2_table1_part2_query(year):
    query = f"""
    SELECT
        p.category_id,
        IFNULL(SUM(CASE WHEN strftime('%m', o.date) = '01' THEN oi.quantity * p.supplier_package_size ELSE 0 END), 0) as Jan,
        IFNULL(SUM(CASE WHEN strftime('%m', o.date) = '02' THEN oi.quantity * p.supplier_package_size ELSE 0 END), 0) as Feb,
        IFNULL(SUM(CASE WHEN strftime('%m', o.date) = '03' THEN oi.quantity * p.supplier_package_size ELSE 0 END), 0) as Mar,
        IFNULL(SUM(CASE WHEN strftime('%m', o.date) = '04' THEN oi.quantity * p.supplier_package_size ELSE 0 END), 0) as Apr,
        IFNULL(SUM(CASE WHEN strftime('%m', o.date) = '05' THEN oi.quantity * p.supplier_package_size ELSE 0 END), 0) as May,
        IFNULL(SUM(CASE WHEN strftime('%m', o.date) = '06' THEN oi.quantity * p.supplier_package_size ELSE 0 END), 0) as Jun,
        IFNULL(SUM(CASE WHEN strftime('%m', o.date) = '07' THEN oi.quantity * p.supplier_package_size ELSE 0 END), 0) as Jul,
        IFNULL(SUM(CASE WHEN strftime('%m', o.date) = '08' THEN oi.quantity * p.supplier_package_size ELSE 0 END), 0) as Aug,
        IFNULL(SUM(CASE WHEN strftime('%m', o.date) = '09' THEN oi.quantity * p.supplier_package_size ELSE 0 END), 0) as Sep,
        IFNULL(SUM(CASE WHEN strftime('%m', o.date) = '10' THEN oi.quantity * p.supplier_package_size ELSE 0 END), 0) as Oct,
        IFNULL(SUM(CASE WHEN strftime('%m', o.date) = '11' THEN oi.quantity * p.supplier_package_size ELSE 0 END), 0) as Nov,
        IFNULL(SUM(CASE WHEN strftime('%m', o.date) = '12' THEN oi.quantity * p.supplier_package_size ELSE 0 END), 0) as Dec
        -- Total column with IFNULL
        --,IFNULL(SUM(oi.quantity * p.supplier_package_size), 0) as Total
    FROM products p
    LEFT JOIN order_items oi ON p.id = oi.product_id
    LEFT JOIN orders o ON o.id = oi.order_id AND strftime('%Y', o.date) = '{year}' AND o.status = 'completed'
    GROUP BY p.category_id
    ORDER BY p.category_id;
    """
    return query


def get_form2_table2_query(year):
    query = f"""
    SELECT
pc.id AS category_id,
IFNULL(SUM(CASE WHEN strftime('%m', fe.date) = '01' THEN fi.quantity * p.package_size ELSE 0 END), 0) as Jan,
IFNULL(SUM(CASE WHEN strftime('%m', fe.date) = '02' THEN fi.quantity * p.package_size ELSE 0 END), 0) as Feb,
IFNULL(SUM(CASE WHEN strftime('%m', fe.date) = '03' THEN fi.quantity * p.package_size ELSE 0 END), 0) as Mar,
IFNULL(SUM(CASE WHEN strftime('%m', fe.date) = '04' THEN fi.quantity * p.package_size ELSE 0 END), 0) as Apr,
IFNULL(SUM(CASE WHEN strftime('%m', fe.date) = '05' THEN fi.quantity * p.package_size ELSE 0 END), 0) as May,
IFNULL(SUM(CASE WHEN strftime('%m', fe.date) = '06' THEN fi.quantity * p.package_size ELSE 0 END), 0) as Jun,
IFNULL(SUM(CASE WHEN strftime('%m', fe.date) = '07' THEN fi.quantity * p.package_size ELSE 0 END), 0) as Jul,
IFNULL(SUM(CASE WHEN strftime('%m', fe.date) = '08' THEN fi.quantity * p.package_size ELSE 0 END), 0) as Aug,
IFNULL(SUM(CASE WHEN strftime('%m', fe.date) = '09' THEN fi.quantity * p.package_size ELSE 0 END), 0) as Sep,
IFNULL(SUM(CASE WHEN strftime('%m', fe.date) = '10' THEN fi.quantity * p.package_size ELSE 0 END), 0) as Oct,
IFNULL(SUM(CASE WHEN strftime('%m', fe.date) = '11' THEN fi.quantity * p.package_size ELSE 0 END), 0) as Nov,
IFNULL(SUM(CASE WHEN strftime('%m', fe.date) = '12' THEN fi.quantity * p.package_size ELSE 0 END), 0) as Dec
-- Total column with IFNULL
--,IFNULL(SUM(fi.quantity * p.package_size), 0) as Total
FROM product_categories pc 
LEFT JOIN products p ON p.category_id = pc.id 
LEFT JOIN field_items fi ON p.id = fi.product_id 
LEFT JOIN field_event fe ON fi.event_id = fe.id AND strftime('%Y', fe.date) = '{year}'
GROUP BY pc.id 
ORDER BY pc.id
    """
    return query


def get_form3_table1_query(month_number, year):
    start_date_str, end_date_str = get_start_and_end_dates(month_number, year)

    # SQL query with the correct date range
    query = f"""
    SELECT
        sp.permit,
        s.name AS supplier_name,
        strftime('%d', o.date) || '-' ||
        substr('JanFebMarAprMayJunJulAugSepOctNovDec', (strftime('%m', o.date) - 1) * 3 + 1, 3) || '-' ||
        substr(strftime('%Y', o.date), 3, 2) AS formatted_date
    FROM orders o
    INNER JOIN suppliers s
        ON o.supplier_id = s.id
    INNER JOIN supplier_permits sp
        ON o.supplier_id = sp.supplier_id
    WHERE o.date >= '{start_date_str}'
      AND o.date < '{end_date_str}'
      AND o.status = 'completed'
    GROUP BY sp.permit, o.date
    ORDER BY o.date ASC;
    """
    return query


def get_form3_table3_query(month_number, year):
    formatted_month = str(month_number).zfill(2)  # This will return '09'

    # SQL query with the correct date range
    query = f"""
    SELECT
    strftime('%d', fe.date) || '-' ||
    substr('JanFebMarAprMayJunJulAugSepOctNovDec', (strftime('%m', fe.date) - 1) * 3 + 1, 3) AS fecha,
    ROW_NUMBER() OVER (ORDER BY fe.date) AS num_voladura,
    l.name AS lugar_exacto,
    SUM(CASE WHEN p.category_id = 1 THEN p.package_size * fi.quantity ELSE 0 END) AS product1_quantity_used,
    SUM(CASE WHEN p.category_id = 2 THEN p.package_size * fi.quantity ELSE 0 END) AS product2_quantity_used,
    SUM(CASE WHEN p.category_id = 3 THEN p.package_size * fi.quantity ELSE 0 END) AS product3_quantity_used,
    SUM(CASE WHEN p.category_id = 4 THEN p.package_size * fi.quantity ELSE 0 END) AS product4_quantity_used,
    SUM(CASE WHEN p.category_id = 5 THEN p.package_size * fi.quantity ELSE 0 END) AS product5_quantity_used
FROM field_items fi
LEFT JOIN field_event fe ON fi.event_id = fe.id 
LEFT JOIN locations l ON fe.location_id = l.id 
LEFT JOIN products p ON fi.product_id = p.id 
WHERE strftime('%Y', fe.date) = '{year}' AND strftime('%m', fe.date) = '{formatted_month}'
GROUP BY fi.event_id, fe.date, l.name
ORDER BY fe.date;
    """
    return query
