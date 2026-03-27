SELECT 
    DATE(timestamp) AS Day,
    COUNT(*) AS Transaction_Count,
    ROUND(SUM(amount),2) AS Aggregate_Daily_Totals
FROM transactions
WHERE status = 'completed'
GROUP BY Day
ORDER BY Day;
