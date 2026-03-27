SELECT 
    DATE(timestamp) AS Day,
    COUNT(*) AS Transaction_Count
FROM transactions
GROUP BY Day
ORDER BY Day;
