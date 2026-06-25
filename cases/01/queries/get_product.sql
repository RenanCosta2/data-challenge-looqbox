SELECT 
	* 
FROM 
	`looqbox-challenge`.data_product_sales
WHERE
	PRODUCT_CODE = {product_code} AND
    STORE_CODE = {store_code} AND
    (
    DATE >= '{start_date}' AND
    DATE <= '{end_date}'
    )