SELECT title FROM movies INNER JOIN stars ON stars.movie_id = movies.id INNER JOIN people ON people.id = stars.person_id WHERE people.name = 'Johnny Depp'
intersect
SELECT title FROM movies INNER JOIN stars ON stars.movie_id = movies.id INNER JOIN people ON people.id = stars.person_id WHERE people.name = 'Helena Bonham Carter';