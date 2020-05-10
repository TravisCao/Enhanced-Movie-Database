




-- ===========================================================================================================================================================================
-- ===========================================================================================================================================================================
-- ===========================================================================================================================================================================
-- ===========================================================================================================================================================================

-- Movie's Production Area, Rating and Box Office
-- CREATE VIEW area_rating_money AS
-- SELECT area_rating.Mid, area_rating.Area, area_rating.rating, Movie_Box_Office_Total
-- FROM ( SELECT movie_basic_info.Mid, Area, rating FROM movie_basic_info, movie_area WHERE movie_area.Mid = movie_basic_info.Mid ) 
-- as area_rating, movie_box_office_total
-- WHERE movie_box_office_total.Mid = area_rating.Mid ;

-- Movie's Rating and Box Office
-- CREATE VIEW rating_money AS
-- SELECT Mid, AVG(rating), AVG(Movie_Box_Office_Total)
-- FROM area_rating_money
-- GROUP BY Mid;

-- Actor's Rating and Box Office
-- CREATE VIEW actor_rating_money AS
-- SELECT Actors_Movie.Mid, Aid, average_rating, average_Movie_Box_Office_Total
-- FROM rating_money, Actors_Movie
-- WHERE rating_money.Mid = Actors_Movie.Mid;

-- Movie, Actor, Rating
-- CREATE VIEW movie_actor_rating AS
-- SELECT movie_basic_info.Mid, title, rating, Aid, profession
-- FROM movie_basic_info, Actors_Movie
-- WHERE movie_basic_info.Mid = Actors_Movie.Mid
-- ===========================================================================================================================================================================
-- ===========================================================================================================================================================================
-- ===========================================================================================================================================================================
-- ===========================================================================================================================================================================



-- 年均评分变化
-- SELECT year, AVG(rating), COUNT(rating)
-- FROM movie_basic_info
-- GROUP BY(year);


-- 类型电影年均评分变化
-- SELECT year, Category, AVG(rating)
-- FROM movie_basic_info, movie_category
-- WHERE movie_category.Category = '剧情' AND movie_category.Mid = movie_basic_info.Mid
-- GROUP BY(movie_basic_info.year);


-- 特定地区 电影年均评分变化
-- SELECT year, Area, COUNT(rating)
-- FROM movie_basic_info, movie_area
-- WHERE movie_area.Area = '英国' AND movie_area.Mid = movie_basic_info.Mid
-- GROUP BY(year);


-- 每个地区的电影平均票房及平均分数
-- SELECT area_rating.Area, AVG(area_rating.rating), AVG(Movie_Box_Office_Total)
-- FROM ( SELECT movie_basic_info.Mid, Area, rating FROM movie_basic_info, movie_area WHERE movie_area.Mid = movie_basic_info.Mid ) as area_rating, movie_box_office_total
-- WHERE movie_box_office_total.Mid = area_rating.Mid
-- GROUP BY area_rating.Area

-- SELECT year, AVG(movie_basic_info.rating), SUM(Movie_Box_Office_Total)
-- FROM movie_basic_info, movie_box_office_total
-- WHERE movie_box_office_total.Mid = movie_basic_info.Mid
-- GROUP BY movie_basic_info.year



-- 有票房记录的影片中，每个演员的作品平均分及平均票房收入
-- SELECT Actors_info.C_name, Actors_info.E_name, AVG(average_rating), SUM(average_Movie_Box_Office_Total)
-- FROM actor_rating_money, Actors_info
-- WHERE actor_rating_money.Aid = Actors_info.Aid
-- GROUP BY C_name, E_name

-- SELECT Actors_info.C_name, average_rating, average_Movie_Box_Office_Total
-- FROM actor_rating_money, Actors_info
-- WHERE actor_rating_money.Aid = Actors_info.Aid



-- 演员里，电影平均分排名
-- SELECT  AVG(rating), C_name
-- FROM movie_actor_rating, Actors_info
-- WHERE movie_actor_rating.Aid = Actors_info.Aid AND profession = "演员"
-- GROUP BY C_name


-- ===========================================================================================================================================================================

-- 演员里，电影平均分排名

-- CREATE VIEW country_725actor AS
-- SELECT  COUNT(Actors_info.Aid), Country
-- FROM movie_actor_rating, Actors_info
-- WHERE movie_actor_rating.Aid = Actors_info.Aid AND profession = "演员" AND rating > 7.25
-- GROUP BY Country;

-- CREATE VIEW country_0actor AS
-- SELECT  COUNT(Actors_info.Aid), Country
-- FROM movie_actor_rating, Actors_info
-- WHERE movie_actor_rating.Aid = Actors_info.Aid AND profession = "演员" 
-- GROUP BY E_name, C_name, Country;


-- SELECT  number725_Actors/number0_Actors,country_725actor.country
-- FROM country_725actor, country_0actor
-- WHERE country_0actor.country = country_725actor.country



-- ===========================================================================================================================================================================

-- SELECT  movie_basic_info.Mid, title, Area
-- FROM movie_basic_info, movie_area
-- WHERE movie_basic_info.Mid = movie_area.Mid AND rating > 7.25
-- GROUP BY E_name, C_name, Country

-- 总观影人数最多的电影
-- SELECT movie_basic_info.Mid, movie_basic_info.title, SUM(Total_Audience_1M)
-- FROM movie_basic_info, movie_box_office
-- WHERE movie_basic_info.Mid = movie_box_office.Mid
-- GROUP BY movie_basic_info.Mid


-- SELECT COUNT(rating), Country
-- FROM movie_actor_rating, Actors_info
-- WHERE movie_actor_rating.Aid = Actors_info.Aid AND profession = "演员" 
-- GROUP BY Country






-- 电影类型数量统计 及类型的平均分
-- SELECT  movie_category.Category, COUNT(distinct movie_category.Mid), AVG(rating) -- COUNT(movie_basic.Mid)
-- FROM movie_basic_info, movie_category
-- WHERE movie_basic_info.Mid =  movie_category.Mid 
-- GROUP BY movie_category.Category;




-- 导演或者演员作品平均分排名
-- SELECT Actors_info.C_name, Actors_info.E_name, movie_basic.Title, AVG(movie_basic.Rating)
-- FROM movie_basic, Actors_Movie, Actors_info
-- WHERE movie_basic.Mid =  Actors_Movie.Mid AND Actors_info.Aid = Actors_Movie.Aid 
-- GROUP BY Actors_info.E_name;
