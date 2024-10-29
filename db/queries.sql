-- Last quantity on inventory
SELECT previous_existence + bought - consumed
FROM Inventory
WHERE product_id = 1
ORDER BY date DESC
LIMIT 1;

-- bought
SELECT SUM(ti.quantity * p.package_size) AS out
FROM TransactionItems ti
JOIN Products p ON ti.product_id = p.id
WHERE ti.transaction_id IN (
    SELECT t.id FROM Transactions t
    WHERE t.date >= '2024-10-01'
    AND t.type = 'in'
)
AND ti.product_id = 1;

-- consumed
SELECT SUM(ti.quantity * p.package_size) AS out
FROM TransactionItems ti
JOIN Products p ON ti.product_id = p.id
WHERE ti.transaction_id IN (
    SELECT t.id FROM Transactions t
    WHERE t.date >= '2024-10-01'
    AND t.type = 'out'
)
AND ti.product_id = 1;

-- returned from field to warehouse
SELECT SUM(ti.quantity * p.package_size) AS out
FROM TransactionItems ti
JOIN Products p ON ti.product_id = p.id
WHERE ti.transaction_id IN (
    SELECT t.id FROM Transactions t
    WHERE t.date >= '2024-10-01'
    AND t.type = 'return'
)
AND ti.product_id = 1;
