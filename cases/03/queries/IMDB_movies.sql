SELECT
    *
FROM
    `looqbox-challenge`.IMDB_movies
WHERE
	RevenueMillions IS NOT NULL AND
    Votes > (
		SELECT
			AVG(Votes)
		FROM
			`looqbox-challenge`.IMDB_movies
    )