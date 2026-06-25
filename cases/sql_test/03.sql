SELECT 
	BUSINESS_NAME,
	SUM(SALES_VALUE) AS TOTAL_SALES
FROM 
	`looqbox-challenge`.data_store_cad AS store
JOIN
	`looqbox-challenge`.data_product_sales AS sales
    USING(STORE_CODE)
WHERE 
	sales.DATE >= '2019-01-01' AND
    sales.DATE < '2019-04-01'
GROUP BY
	BUSINESS_NAME