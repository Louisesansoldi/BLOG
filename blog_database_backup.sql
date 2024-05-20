-- MariaDB dump 10.19-11.2.2-MariaDB, for osx10.17 (x86_64)
--
-- Host: localhost    Database: blog_database
-- ------------------------------------------------------
-- Server version	11.2.2-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `comments`
--

DROP TABLE IF EXISTS `comments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `comments` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `contentComments` varchar(255) NOT NULL,
  `dateTime` datetime DEFAULT NULL,
  `users_id` int(11) DEFAULT NULL,
  `posts_id` int(11) DEFAULT NULL,
  `user_name` char(30) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `users_id` (`users_id`),
  KEY `posts_id` (`posts_id`),
  KEY `user_name` (`user_name`),
  CONSTRAINT `comments_ibfk_1` FOREIGN KEY (`users_id`) REFERENCES `users` (`id`),
  CONSTRAINT `comments_ibfk_2` FOREIGN KEY (`posts_id`) REFERENCES `posts` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comments`
--

LOCK TABLES `comments` WRITE;
/*!40000 ALTER TABLE `comments` DISABLE KEYS */;
INSERT INTO `comments` VALUES
(1,'yoooooo, j\'adore trop',NULL,NULL,NULL,'lou'),
(2,'yoooooo, j\'adore trop',NULL,NULL,NULL,'1'),
(3,'yoooooo, j\'adore trop',NULL,1,NULL,'lou'),
(4,'yoooooo, j\'adore trop',NULL,1,1,'lou'),
(5,'yoooooo, j\'adore trop',NULL,1,2,'lou'),
(6,'yoooooo, j\'adore trop',NULL,1,1,'lou'),
(7,'yoooooo, j\'adore trop et encore plus',NULL,1,1,'lou');
/*!40000 ALTER TABLE `comments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `interactions`
--

DROP TABLE IF EXISTS `interactions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `interactions` (
  `interaction_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `post_id` int(11) DEFAULT NULL,
  `interaction_type` enum('like','share','comment') DEFAULT NULL,
  `interaction_date` datetime DEFAULT NULL,
  PRIMARY KEY (`interaction_id`),
  KEY `user_id` (`user_id`),
  KEY `post_id` (`post_id`),
  CONSTRAINT `interactions_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `interactions_ibfk_2` FOREIGN KEY (`post_id`) REFERENCES `posts` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `interactions`
--

LOCK TABLES `interactions` WRITE;
/*!40000 ALTER TABLE `interactions` DISABLE KEYS */;
/*!40000 ALTER TABLE `interactions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `likes`
--

DROP TABLE IF EXISTS `likes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `likes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `posts_id` int(11) DEFAULT NULL,
  `likes_count` int(11) DEFAULT 0,
  PRIMARY KEY (`id`),
  KEY `fk_likes_posts` (`posts_id`),
  CONSTRAINT `fk_likes_posts` FOREIGN KEY (`posts_id`) REFERENCES `posts` (`id`) ON DELETE CASCADE,
  CONSTRAINT `likes_ibfk_1` FOREIGN KEY (`posts_id`) REFERENCES `posts` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `likes`
--

LOCK TABLES `likes` WRITE;
/*!40000 ALTER TABLE `likes` DISABLE KEYS */;
INSERT INTO `likes` VALUES
(1,4,1),
(2,4,1),
(3,4,1),
(4,4,1),
(5,4,1),
(6,2,1),
(7,4,1);
/*!40000 ALTER TABLE `likes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `posts`
--

DROP TABLE IF EXISTS `posts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `posts` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `content` text DEFAULT NULL,
  `link` text DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `universe_id` int(11) DEFAULT NULL,
  `imageUrl` varchar(255) DEFAULT NULL,
  `canvaUrl` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `universe_id` (`universe_id`),
  CONSTRAINT `posts_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `posts_ibfk_2` FOREIGN KEY (`universe_id`) REFERENCES `universe` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `posts`
--

LOCK TABLES `posts` WRITE;
/*!40000 ALTER TABLE `posts` DISABLE KEYS */;
INSERT INTO `posts` VALUES
(1,'dolphins everywhere','Dolphins are highly intelligent marine mammals and are part of the family of toothed whales that includes orcas and pilot whales.','https://www.google.com/search?q=dolphins+gif&client=safari&sca_esv=87522dea2824ff52&sca_upv=1&rls=en&sxsrf=ADLYWILGX5OhQ8vuoGHZaCC8LTZ6gT4a7A%3A1715080540584&ei=XA06ZuehI5GTkdUPt5aAuAY&ved=0ahUKEwjnv4fztPuFAxWRSaQEHTcLAGcQ4dUDCA8&uact=5&oq=dolphins+gif&gs_lp=Egxnd3Mtd2l6LXNlcnAiDGRvbHBoaW5zIGdpZjIIEAAYgAQYywEyCBAAGIAEGMsBMggQABiABBjLATIIEAAYgAQYywEyCBAAGIAEGMsBMggQABiABBjLATIIEAAYgAQYywEyCBAAGIAEGMsBMggQABiABBjLATIIEAAYgAQYywFIkx1QAFjkEnAAeAGQAQCYAVWgAawDqgEBNrgBA8gBAPgBAZgCBqAC9APCAgoQLhiABBhDGIoFwgIGEAAYBxgewgIZEC4YgAQYQxiKBRiXBRjcBBjeBBjgBNgBAcICCxAuGIAEGMcBGK8BwgIFEAAYgATCAggQLhiABBjLAcICBRAuGIAEwgIUEC4YgAQYlwUY3AQY3gQY4ATYAQHCAg0QLhiABBjHARgKGK8BmAMAugYGCAEQARgUkgcDNS4xoAeSOA&sclient=gws-wiz-serp',NULL,NULL,NULL,NULL),
(2,'dolphins everywhere','Dolphins are highly intelligent marine mammals and are part of the family of toothed whales that includes orcas and pilot whales.','https://www.google.com/search?q=dolphins+gif&client=safari&sca_esv=87522dea2824ff52&sca_upv=1&rls=en&sxsrf=ADLYWILGX5OhQ8vuoGHZaCC8LTZ6gT4a7A%3A1715080540584&ei=XA06ZuehI5GTkdUPt5aAuAY&ved=0ahUKEwjnv4fztPuFAxWRSaQEHTcLAGcQ4dUDCA8&uact=5&oq=dolphins+gif&gs_lp=Egxnd3Mtd2l6LXNlcnAiDGRvbHBoaW5zIGdpZjIIEAAYgAQYywEyCBAAGIAEGMsBMggQABiABBjLATIIEAAYgAQYywEyCBAAGIAEGMsBMggQABiABBjLATIIEAAYgAQYywEyCBAAGIAEGMsBMggQABiABBjLATIIEAAYgAQYywFIkx1QAFjkEnAAeAGQAQCYAVWgAawDqgEBNrgBA8gBAPgBAZgCBqAC9APCAgoQLhiABBhDGIoFwgIGEAAYBxgewgIZEC4YgAQYQxiKBRiXBRjcBBjeBBjgBNgBAcICCxAuGIAEGMcBGK8BwgIFEAAYgATCAggQLhiABBjLAcICBRAuGIAEwgIUEC4YgAQYlwUY3AQY3gQY4ATYAQHCAg0QLhiABBjHARgKGK8BmAMAugYGCAEQARgUkgcDNS4xoAeSOA&sclient=gws-wiz-serp',NULL,NULL,NULL,NULL),
(3,'dolphins everywhere','Dolphins are highly intelligent marine mammals and are part of the family of toothed whales that includes orcas and pilot whales.','https://www.google.com/search?q=dolphins+gif&client=safari&sca_esv=87522dea2824ff52&sca_upv=1&rls=en&sxsrf=ADLYWILGX5OhQ8vuoGHZaCC8LTZ6gT4a7A%3A1715080540584&ei=XA06ZuehI5GTkdUPt5aAuAY&ved=0ahUKEwjnv4fztPuFAxWRSaQEHTcLAGcQ4dUDCA8&uact=5&oq=dolphins+gif&gs_lp=Egxnd3Mtd2l6LXNlcnAiDGRvbHBoaW5zIGdpZjIIEAAYgAQYywEyCBAAGIAEGMsBMggQABiABBjLATIIEAAYgAQYywEyCBAAGIAEGMsBMggQABiABBjLATIIEAAYgAQYywEyCBAAGIAEGMsBMggQABiABBjLATIIEAAYgAQYywFIkx1QAFjkEnAAeAGQAQCYAVWgAawDqgEBNrgBA8gBAPgBAZgCBqAC9APCAgoQLhiABBhDGIoFwgIGEAAYBxgewgIZEC4YgAQYQxiKBRiXBRjcBBjeBBjgBNgBAcICCxAuGIAEGMcBGK8BwgIFEAAYgATCAggQLhiABBjLAcICBRAuGIAEwgIUEC4YgAQYlwUY3AQY3gQY4ATYAQHCAg0QLhiABBjHARgKGK8BmAMAugYGCAEQARgUkgcDNS4xoAeSOA&sclient=gws-wiz-serp',NULL,NULL,NULL,NULL),
(4,'dolphins everywhere','Dolphins are highly intelligent marine mammals and are part of the family of toothed whales that includes orcas and pilot whales.','hohohohohohoho',NULL,NULL,NULL,NULL),
(5,'dolphins everywhere','Dolphins are highly intelligent marine mammals and are part of the family of toothed whales that includes orcas and pilot whales.','hohohohohohoho',NULL,NULL,NULL,NULL),
(6,'dolphins everywhere','Dolphins are highly intelligent marine mammals and are part of the family of toothed whales that includes orcas and pilot whales.','hohohohohohoho',1,NULL,NULL,NULL),
(7,'dolphins everywhere','Dolphins are highly intelligent marine mammals and are part of the family of toothed whales that includes orcas and pilot whales.','hohohohohohoho',1,NULL,NULL,NULL),
(9,'dolphins everywhere','Dolphins are highly intelligent marine mammals and are part of the family of toothed whales that includes orcas and pilot whales.','hohohohohohoho',1,13,'this is the url',NULL),
(10,'title post','content post','link post',1,13,'https://res.cloudinary.com/ddw3sbubm/image/upload/v1715938422/hmijjbt6zncxjpbmzbmj.jpg',NULL),
(12,'title post','content post','link post',1,13,'https://res.cloudinary.com/ddw3sbubm/image/upload/v1715940151/am8ttiudq7gj4myflhbw.jpg',NULL),
(13,'title post','content post','link post',1,13,'https://res.cloudinary.com/ddw3sbubm/image/upload/v1715942168/eo4wg56xhjiqujgsgbai.jpg','https://res.cloudinary.com/ddw3sbubm/image/upload/v1715942169/opqpcfc545amb5id1d9g.jpg'),
(14,'dolphins everywhere','https://www.google.com/search?q=dolphins+gif&client=safari&sca_esv=87522dea2824ff52&sca_upv=1&rls=en&sxsrf=ADLYWILGX5OhQ8vuoGHZaCC8LTZ6gT4a7A%3A1715080540584&ei=XA06ZuehI5GTkdUPt5aAuAY&ved=0ahUKEwjnv4fztPuFAxWRSaQEHTcLAGcQ4dUDCA8&uact=5&oq=dolphins+gif&gs_lp=Egxnd3Mtd2l6LXNlcnAiDGRvbHBoaW5zIGdpZjIIEAAYgAQYywEyCBAAGIAEGMsBMggQABiABBjLATIIEAAYgAQYywEyCBAAGIAEGMsBMggQABiABBjLATIIEAAYgAQYywEyCBAAGIAEGMsBMggQABiABBjLATIIEAAYgAQYywFIkx1QAFjkEnAAeAGQAQCYAVWgAawDqgEBNrgBA8gBAPgBAZgCBqAC9APCAgoQLhiABBhDGIoFwgIGEAAYBxgewgIZEC4YgAQYQxiKBRiXBRjcBBjeBBjgBNgBAcICCxAuGIAEGMcBGK8BwgIFEAAYgATCAggQLhiABBjLAcICBRAuGIAEwgIUEC4YgAQYlwUY3AQY3gQY4ATYAQHCAg0QLhiABBjHARgKGK8BmAMAugYGCAEQARgUkgcDNS4xoAeSOA&sclient=gws-wiz-serp',NULL,1,14,'Dolphins are highly intelligent marine mammals and are part of the family of toothed whales that includes orcas and pilot whales.',NULL),
(15,'dolphins everywhere','https://www.google.com/search?q=dolphins+gif&client=safari&sca_esv=87522dea2824ff52&sca_upv=1&rls=en&sxsrf=ADLYWILGX5OhQ8vuoGHZaCC8LTZ6gT4a7A%3A1715080540584&ei=XA06ZuehI5GTkdUPt5aAuAY&ved=0ahUKEwjnv4fztPuFAxWRSaQEHTcLAGcQ4dUDCA8&uact=5&oq=dolphins+gif&gs_lp=Egxnd3Mtd2l6LXNlcnAiDGRvbHBoaW5zIGdpZjIIEAAYgAQYywEyCBAAGIAEGMsBMggQABiABBjLATIIEAAYgAQYywEyCBAAGIAEGMsBMggQABiABBjLATIIEAAYgAQYywEyCBAAGIAEGMsBMggQABiABBjLATIIEAAYgAQYywFIkx1QAFjkEnAAeAGQAQCYAVWgAawDqgEBNrgBA8gBAPgBAZgCBqAC9APCAgoQLhiABBhDGIoFwgIGEAAYBxgewgIZEC4YgAQYQxiKBRiXBRjcBBjeBBjgBNgBAcICCxAuGIAEGMcBGK8BwgIFEAAYgATCAggQLhiABBjLAcICBRAuGIAEwgIUEC4YgAQYlwUY3AQY3gQY4ATYAQHCAg0QLhiABBjHARgKGK8BmAMAugYGCAEQARgUkgcDNS4xoAeSOA&sclient=gws-wiz-serp',NULL,1,14,'Dolphins are highly intelligent marine mammals and are part of the family of toothed whales that includes orcas and pilot whales.',NULL),
(16,'title post','link post','1',1,14,'content post','https://res.cloudinary.com/ddw3sbubm/image/upload/v1715942168/eo4wg56xhjiqujgsgbai.jpg'),
(17,'dolphins everywhere','https://www.google.com/search?q=dolphins+gif&client=safari&sca_esv=87522dea2824ff52&sca_upv=1&rls=en&sxsrf=ADLYWILGX5OhQ8vuoGHZaCC8LTZ6gT4a7A%3A1715080540584&ei=XA06ZuehI5GTkdUPt5aAuAY&ved=0ahUKEwjnv4fztPuFAxWRSaQEHTcLAGcQ4dUDCA8&uact=5&oq=dolphins+gif&gs_lp=Egxnd3Mtd2l6LXNlcnAiDGRvbHBoaW5zIGdpZjIIEAAYgAQYywEyCBAAGIAEGMsBMggQABiABBjLATIIEAAYgAQYywEyCBAAGIAEGMsBMggQABiABBjLATIIEAAYgAQYywEyCBAAGIAEGMsBMggQABiABBjLATIIEAAYgAQYywFIkx1QAFjkEnAAeAGQAQCYAVWgAawDqgEBNrgBA8gBAPgBAZgCBqAC9APCAgoQLhiABBhDGIoFwgIGEAAYBxgewgIZEC4YgAQYQxiKBRiXBRjcBBjeBBjgBNgBAcICCxAuGIAEGMcBGK8BwgIFEAAYgATCAggQLhiABBjLAcICBRAuGIAEwgIUEC4YgAQYlwUY3AQY3gQY4ATYAQHCAg0QLhiABBjHARgKGK8BmAMAugYGCAEQARgUkgcDNS4xoAeSOA&sclient=gws-wiz-serp',NULL,1,14,'Dolphins are highly intelligent marine mammals and are part of the family of toothed whales that includes orcas and pilot whales.',NULL),
(18,'7','Dolphins are highly intelligent marine mammals and are part of the family of toothed whales that includes orcas and pilot whales.','hohohohohohoho',1,14,'dolphins everywhere',NULL),
(19,'dolphins everywhere','Dolphins are highly intelligent marine mammals and are part of the family of toothed whales that includes orcas and pilot whales.','hohohohohohoho',1,14,'this is the url',NULL),
(20,'dolphins everywhere','Dolphins are highly intelligent marine mammals and are part of the family of toothed whales that includes orcas and pilot whales.','hohohohohohoho',1,14,'this is the url',NULL),
(21,'dolphins everywhere','Dolphins are highly intelligent marine mammals and are part of the family of toothed whales that includes orcas and pilot whales.','hohohohohohoho',1,14,'this is the url',NULL),
(22,'title post','content post','link post',1,13,'https://res.cloudinary.com/ddw3sbubm/image/upload/v1715949899/d4wpp6g9kv47ghdcgnzb.jpg','https://res.cloudinary.com/ddw3sbubm/image/upload/v1715949900/lertqylugmbzoimawosl.jpg'),
(23,'title post','content post','link post',1,14,'https://res.cloudinary.com/ddw3sbubm/image/upload/v1715949899/d4wpp6g9kv47ghdcgnzb.jpg','https://res.cloudinary.com/ddw3sbubm/image/upload/v1715949900/lertqylugmbzoimawosl.jpg'),
(24,'title post','content post','link post',1,13,'https://res.cloudinary.com/ddw3sbubm/image/upload/v1716212499/yngerzxsdfz6nwgpxtmi.jpg','https://res.cloudinary.com/ddw3sbubm/image/upload/v1716212500/s86fvtzqlkxttaogm3fm.jpg');
/*!40000 ALTER TABLE `posts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `universe`
--

DROP TABLE IF EXISTS `universe`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `universe` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `titleUniverse` varchar(255) NOT NULL,
  `descriptionUniverse` varchar(255) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `backgroundUniverse` varchar(255) DEFAULT NULL,
  `backgroundTitle` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `universe_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `universe`
--

LOCK TABLES `universe` WRITE;
/*!40000 ALTER TABLE `universe` DISABLE KEYS */;
INSERT INTO `universe` VALUES
(13,'my universe','it\'s an amazing universe',1,'image',NULL),
(14,'my universe','it\'s an amazing universe',1,'image',NULL),
(15,'my super universe','it\'s an amazing universe',1,'image',NULL),
(16,'title','description',1,'https://res.cloudinary.com/ddw3sbubm/image/upload/v1715937354/nwb4roy7ncybvff7v7vc.jpg',NULL),
(17,'title','description ehehe',1,'https://res.cloudinary.com/ddw3sbubm/image/upload/v1715938114/ultxiyf5o262fqgdyagv.jpg',NULL);
/*!40000 ALTER TABLE `universe` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` char(30) NOT NULL,
  `email` varchar(255) NOT NULL DEFAULT '',
  `password` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES
(1,'lou','loulou@gmail.com','$2b$12$NCXpPFvnoeKGzcPGyzbboOH.Q3VPwxIxxWMAYM56XtjNm36UKMQem'),
(2,'lou','loulou@gmail.com','$2b$12$.eelp27AFK8ybrhn5RYyZ.SKlVqQ7UpYpLS6o1MN0JFls7wdRaa1W');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-05-20 17:41:07
