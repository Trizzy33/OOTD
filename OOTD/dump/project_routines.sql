-- MySQL dump 10.13  Distrib 8.0.27, for Win64 (x86_64)
--
-- Host: localhost    Database: project
-- ------------------------------------------------------
-- Server version	8.0.27

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Dumping routines for database 'project'
--
/*!50003 DROP PROCEDURE IF EXISTS `lucky_user` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `lucky_user`()
BEGIN
	declare userIdBlog int;
    declare userIdOutfit int;
    
    declare blogCursor cursor for 
    select user_id
	from user join blog on user_id = author_id
	group by user_id
	having count(id) >= 1
    ;
    
	declare outfitCursor cursor for 
    select user.user_id
	from user join outfits on user.user_id = outfits.user_id
	group by user_id
	having count(id) >= 1
    ;
    
    drop table if exists blog_user;
    create table blog_user(
    userId int
    );
    
    drop table if exists outfit_user;
    create table outfit_user(
    userId int
    );
    
    open blogCursor;
    begin
    declare exit_flag_blog int default 0;
    declare continue handler for not found set exit_flag_blog = 1;
		bloop:loop
		fetch blogCursor into userIdBlog;
		if userIdBlog = NULL then
			leave bloop;
		elseif exit_flag_blog then
			leave bloop;
		end if;
		
		insert into blog_user values(userIdBlog);
		end loop bloop;
    end;
	close blogCursor;
    
	open outfitCursor;
    begin
    declare exit_flag_outfit int default 0;
    declare continue handler for not found set exit_flag_outfit = 1;
		oloop:loop
		fetch outfitCursor into userIdOutfit;
		if userIdOutfit = NULL then
			leave oloop;
		elseif exit_flag_outfit then
			leave oloop;
		end if;
		
		insert into outfit_user values(userIdOutfit);
		end loop oloop;
    end;
	close outfitCursor;
    
    select user_id, name 
    from blog_user join user on user_id = userId
    where user_id in (select userId from outfit_user)
    order by rand()
    limit 5;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `top_user` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `top_user`()
BEGIN
DECLARE done INT default 0;
    DECLARE ID INT;
    DECLARE UNAME VARCHAR(255);
    DECLARE CNT INT;
    DECLARE cur CURSOR FOR (SELECT u.user_id, u.name, b.cnt
            FROM user u JOIN (SELECT author_id, COUNT(id) AS cnt FROM blog GROUP BY author_id) AS b 
            ON user_id = author_id 
            ORDER BY b.cnt DESC LIMIT 15);
	
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;
    
    DROP TABLE IF EXISTS Top_user;
    
    CREATE TABLE Top_user(
    id INT,
    name  VARCHAR(255),
    cnt INT
    );
    
    OPEN cur;
    REPEAT
		FETCH cur INTO ID, UNAME, CNT;
        INSERT INTO Top_user VALUES (ID, UNAME, CNT);
        UNTIL done
	END REPEAT;
    CLOSE cur;

	SELECT id, name, cnt FROM Top_user ORDER BY cnt DESC;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-12-01 15:46:07
