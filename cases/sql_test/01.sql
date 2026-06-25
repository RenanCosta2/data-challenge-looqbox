WITH ranked_products_by_value AS (
	SELECT 
		*,
		RANK() OVER (ORDER BY PRODUCT_VAL DESC) AS rank_value
	FROM 
		`looqbox-challenge`.data_product 
)

SELECT
	*
FROM
	ranked_products_by_value
WHERE
	rank_value <= 10