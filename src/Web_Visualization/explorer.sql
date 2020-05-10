SELECT Title,
       Rating,
       Category as Genre,
       Reviewer,
       Movie_Box_Office_Total as Box_Office,
       Duration,
       link,
       Year
FROM movie_basic_info as m
INNER JOIN movie_category as c
ON m.Mid = c.Mid
INNER JOIN movie_box_office_total as b
on b.Mid = c.Mid
