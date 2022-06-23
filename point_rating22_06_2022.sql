-- MySQL dump 10.13  Distrib 8.0.28, for Win64 (x86_64)
--
-- Host: localhost    Database: point_rating
-- ------------------------------------------------------
-- Server version	8.0.28

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `activity`
--

DROP TABLE IF EXISTS `activity`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `activity` (
  `id` varchar(32) NOT NULL,
  `name` varchar(60) NOT NULL,
  `user_id` varchar(32) NOT NULL,
  `file` varchar(20) NOT NULL,
  `status` tinyint(1) DEFAULT NULL,
  `comment` varchar(240) DEFAULT NULL,
  `type_id` varchar(32) NOT NULL,
  `rate_id` varchar(32) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `type_id` (`type_id`),
  KEY `rate_id` (`rate_id`),
  CONSTRAINT `activity_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
  CONSTRAINT `activity_ibfk_2` FOREIGN KEY (`type_id`) REFERENCES `activity_type` (`id`),
  CONSTRAINT `activity_ibfk_3` FOREIGN KEY (`rate_id`) REFERENCES `rate_activity` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `activity`
--

LOCK TABLES `activity` WRITE;
/*!40000 ALTER TABLE `activity` DISABLE KEYS */;
INSERT INTO `activity` VALUES ('137292e0daa74756b7d438fdc08f716e','hjkhjkjkl','a4f3737150df495c9dc84aca4efd14b1','668bd2a05bfad70c.pdf',NULL,NULL,'080154b9ed8640fc8191a6fadd352a49','9af07df629cc4853aaea1f320f70fcd4'),('522b08f14d854308be63498f52b257cb','uiouio','a4f3737150df495c9dc84aca4efd14b1','d701f3205d757cdd.pdf',NULL,NULL,'d9af4dd7c72f419296478053dbc39afb','0d70848389ec4fffa7795d6b58cad1b8'),('b42a5e35b6054014a66cf2ba8b7c9897','luiouio','a4f3737150df495c9dc84aca4efd14b1','e847a13b62fe6925.pdf',NULL,NULL,'080154b9ed8640fc8191a6fadd352a49','9af07df629cc4853aaea1f320f70fcd4');
/*!40000 ALTER TABLE `activity` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `activity_sub_type`
--

DROP TABLE IF EXISTS `activity_sub_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `activity_sub_type` (
  `id` varchar(32) NOT NULL,
  `name` varchar(60) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `activity_sub_type`
--

LOCK TABLES `activity_sub_type` WRITE;
/*!40000 ALTER TABLE `activity_sub_type` DISABLE KEYS */;
INSERT INTO `activity_sub_type` VALUES ('28396cc192494572802c680ce9aa4daa','Международный'),('7d06d6b2e1694579a2582eec2ab8512b','Всероссийский'),('894c5a0cdd154d8d9de49a6352f625ec','Республиканский');
/*!40000 ALTER TABLE `activity_sub_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `activity_type`
--

DROP TABLE IF EXISTS `activity_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `activity_type` (
  `id` varchar(32) NOT NULL,
  `name` varchar(60) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `activity_type`
--

LOCK TABLES `activity_type` WRITE;
/*!40000 ALTER TABLE `activity_type` DISABLE KEYS */;
INSERT INTO `activity_type` VALUES ('080154b9ed8640fc8191a6fadd352a49','Научная деятельность'),('1f85fa98e0b04c69a3459c3f016b8c8a','Спортивная деятельность'),('d9af4dd7c72f419296478053dbc39afb','Культурная деятельность'),('e7848cbb291b4327aa047e5b0f383da4','Общественная деятельность');
/*!40000 ALTER TABLE `activity_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `attendance`
--

DROP TABLE IF EXISTS `attendance`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `attendance` (
  `id` varchar(32) NOT NULL,
  `subject_id` varchar(32) NOT NULL,
  `group_id` varchar(32) NOT NULL,
  `type_id` varchar(32) NOT NULL,
  `date` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `subject_id` (`subject_id`),
  KEY `group_id` (`group_id`),
  KEY `type_id` (`type_id`),
  CONSTRAINT `attendance_ibfk_1` FOREIGN KEY (`subject_id`) REFERENCES `subject` (`id`),
  CONSTRAINT `attendance_ibfk_2` FOREIGN KEY (`group_id`) REFERENCES `group` (`id`),
  CONSTRAINT `attendance_ibfk_3` FOREIGN KEY (`type_id`) REFERENCES `attendance_type` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `attendance`
--

LOCK TABLES `attendance` WRITE;
/*!40000 ALTER TABLE `attendance` DISABLE KEYS */;
INSERT INTO `attendance` VALUES ('03ac8076cc2e44aca3602b9742f86f7e','b9ac28dfde2b4bc196a7f09154fe7fef','0684cff744cd406ab9cd35e4d016063a','011a9f2fd59d4f61a98c40ee95a504e8','2021-09-03 00:00:00'),('0abdfd13d4704db6aedfe17657c901da','b9ac28dfde2b4bc196a7f09154fe7fef','ad7ba7cc2ed6425c996426513b2c8bac','8fc97247f8aa4f7c997a335326f15e73','2021-09-29 00:00:00'),('2197ad03a32e4531b41cf90741247d15','c24d76414191419bbfe3a7eca6572262','ad7ba7cc2ed6425c996426513b2c8bac','011a9f2fd59d4f61a98c40ee95a504e8','2021-09-04 00:00:00'),('23d7ceafb3dc4f4eb5c6f09728612c49','b9ac28dfde2b4bc196a7f09154fe7fef','0684cff744cd406ab9cd35e4d016063a','011a9f2fd59d4f61a98c40ee95a504e8','2021-09-14 00:00:00'),('25def2030343484f92beb5cb35ffddab','b9ac28dfde2b4bc196a7f09154fe7fef','ad7ba7cc2ed6425c996426513b2c8bac','8fc97247f8aa4f7c997a335326f15e73','2021-09-21 00:00:00'),('2609a5a006e14c4295e104f6f85a928a','c1cbaa20c7c14209b566e578bbbe8eb9','0684cff744cd406ab9cd35e4d016063a','011a9f2fd59d4f61a98c40ee95a504e8','2021-09-08 00:00:00'),('2a1a8993555d413a80a7eec61c9d89a7','c1cbaa20c7c14209b566e578bbbe8eb9','0684cff744cd406ab9cd35e4d016063a','8fc97247f8aa4f7c997a335326f15e73','2021-09-13 00:00:00'),('3049c43641af49f38aed729c492250d0','b9ac28dfde2b4bc196a7f09154fe7fef','0684cff744cd406ab9cd35e4d016063a','8fc97247f8aa4f7c997a335326f15e73','2021-09-23 00:00:00'),('341090af00de488c924fa9ff7ff22579','b9ac28dfde2b4bc196a7f09154fe7fef','0684cff744cd406ab9cd35e4d016063a','011a9f2fd59d4f61a98c40ee95a504e8','2021-09-10 00:00:00'),('518a0d1b698e4bbfbf84880b4433a1ca','c24d76414191419bbfe3a7eca6572262','ad7ba7cc2ed6425c996426513b2c8bac','8fc97247f8aa4f7c997a335326f15e73','2021-09-15 00:00:00'),('546f21bfe91646d69070a4e429b4380b','c1cbaa20c7c14209b566e578bbbe8eb9','0684cff744cd406ab9cd35e4d016063a','8fc97247f8aa4f7c997a335326f15e73','2021-09-20 00:00:00'),('60f6f3de7a0345d1acb44274c876828a','c1cbaa20c7c14209b566e578bbbe8eb9','0684cff744cd406ab9cd35e4d016063a','011a9f2fd59d4f61a98c40ee95a504e8','2021-09-01 00:00:00'),('77961f4be1f845718669fc25268335e8','c24d76414191419bbfe3a7eca6572262','ad7ba7cc2ed6425c996426513b2c8bac','8fc97247f8aa4f7c997a335326f15e73','2021-09-29 00:00:00'),('81413ce6e2d14e54873d219ec8def861','b9ac28dfde2b4bc196a7f09154fe7fef','0684cff744cd406ab9cd35e4d016063a','8fc97247f8aa4f7c997a335326f15e73','2021-09-16 00:00:00'),('949d34a124c249ad8b8880ae406f50bf','b9ac28dfde2b4bc196a7f09154fe7fef','ad7ba7cc2ed6425c996426513b2c8bac','011a9f2fd59d4f61a98c40ee95a504e8','2021-09-16 00:00:00'),('980bb2107b034baf97bd22eb70171ce4','c1cbaa20c7c14209b566e578bbbe8eb9','0684cff744cd406ab9cd35e4d016063a','8fc97247f8aa4f7c997a335326f15e73','2021-09-27 00:00:00'),('986498d46f664f529d0921300b18691e','c24d76414191419bbfe3a7eca6572262','ad7ba7cc2ed6425c996426513b2c8bac','011a9f2fd59d4f61a98c40ee95a504e8','2021-09-11 00:00:00'),('a052991053e1467f9029a813e2ef68c6','c24d76414191419bbfe3a7eca6572262','ad7ba7cc2ed6425c996426513b2c8bac','011a9f2fd59d4f61a98c40ee95a504e8','2021-09-18 00:00:00'),('dc38f7e739084ad79bf7b756077f001d','b9ac28dfde2b4bc196a7f09154fe7fef','ad7ba7cc2ed6425c996426513b2c8bac','011a9f2fd59d4f61a98c40ee95a504e8','2021-09-02 00:00:00'),('e21b6f5df82d4624b7b15620f07ad9d7','b9ac28dfde2b4bc196a7f09154fe7fef','ad7ba7cc2ed6425c996426513b2c8bac','011a9f2fd59d4f61a98c40ee95a504e8','2021-09-19 00:00:00'),('e30ee1a195494fa7a827827333b69c52','b9ac28dfde2b4bc196a7f09154fe7fef','ad7ba7cc2ed6425c996426513b2c8bac','8fc97247f8aa4f7c997a335326f15e73','2021-09-14 00:00:00'),('e53e1230810346e38eb3822662216c91','c1cbaa20c7c14209b566e578bbbe8eb9','0684cff744cd406ab9cd35e4d016063a','011a9f2fd59d4f61a98c40ee95a504e8','2021-09-15 00:00:00'),('f3dbdfb0704c45cfa4f01a1028666b55','c24d76414191419bbfe3a7eca6572262','ad7ba7cc2ed6425c996426513b2c8bac','8fc97247f8aa4f7c997a335326f15e73','2021-09-22 00:00:00'),('ff8dc49e04304287ba28b34ca29d82d2','b9ac28dfde2b4bc196a7f09154fe7fef','0684cff744cd406ab9cd35e4d016063a','8fc97247f8aa4f7c997a335326f15e73','2021-09-30 00:00:00');
/*!40000 ALTER TABLE `attendance` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `attendance_grade`
--

DROP TABLE IF EXISTS `attendance_grade`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `attendance_grade` (
  `id` varchar(32) NOT NULL,
  `user_id` varchar(32) NOT NULL,
  `attendance_id` varchar(32) NOT NULL,
  `active` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `attendance_id` (`attendance_id`),
  CONSTRAINT `attendance_grade_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
  CONSTRAINT `attendance_grade_ibfk_2` FOREIGN KEY (`attendance_id`) REFERENCES `attendance` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `attendance_grade`
--

LOCK TABLES `attendance_grade` WRITE;
/*!40000 ALTER TABLE `attendance_grade` DISABLE KEYS */;
INSERT INTO `attendance_grade` VALUES ('00645f8756b345f9a5dc10d30d4b9b00','42706fc39cee44ddbbe725d13a4c94d3','518a0d1b698e4bbfbf84880b4433a1ca',0),('03e05c105f4346e1b626803a2043261d','1e6b84723552416e9160ba51082727b1','2a1a8993555d413a80a7eec61c9d89a7',0),('16da227913ce43fb9e28bf315b3beff7','1e6b84723552416e9160ba51082727b1','546f21bfe91646d69070a4e429b4380b',0),('2ae7c43455dd4e559bb7d53b3d5008bc','a4f3737150df495c9dc84aca4efd14b1','e53e1230810346e38eb3822662216c91',0),('3178d62ee2b64798bb9c4168c74da25b','a4f3737150df495c9dc84aca4efd14b1','81413ce6e2d14e54873d219ec8def861',0),('398a83761877465c9f1f2b8a55de54b2','1e6b84723552416e9160ba51082727b1','3049c43641af49f38aed729c492250d0',0),('3ae7d2eb1f424b89b933024875047a9b','42706fc39cee44ddbbe725d13a4c94d3','25def2030343484f92beb5cb35ffddab',0),('3f04fa288f4d4aaa9391b6a074e23478','a4f3737150df495c9dc84aca4efd14b1','980bb2107b034baf97bd22eb70171ce4',0),('54e62cfbc40b496c92f56dd8b0cad840','42706fc39cee44ddbbe725d13a4c94d3','986498d46f664f529d0921300b18691e',0),('71bb09e054f444cdbfd71456a75ee0b3','a4f3737150df495c9dc84aca4efd14b1','60f6f3de7a0345d1acb44274c876828a',0),('741e5e8d9caa4e23accd1708a7ff5519','a4f3737150df495c9dc84aca4efd14b1','03ac8076cc2e44aca3602b9742f86f7e',1),('7d3a380737d64660a727d9cc9e03bf4c','a4f3737150df495c9dc84aca4efd14b1','3049c43641af49f38aed729c492250d0',0),('80a4753c45ea4a5192b6d7e222fd8c2c','a4f3737150df495c9dc84aca4efd14b1','2609a5a006e14c4295e104f6f85a928a',0),('9a715fb5a1cd450592cef616d045df56','a4f3737150df495c9dc84aca4efd14b1','ff8dc49e04304287ba28b34ca29d82d2',0),('9cb36633f1b84d89b1b6b0686e360eb2','a4f3737150df495c9dc84aca4efd14b1','23d7ceafb3dc4f4eb5c6f09728612c49',0),('a585a19b727b4c79aefdee799d6c3e46','42706fc39cee44ddbbe725d13a4c94d3','e30ee1a195494fa7a827827333b69c52',0),('a5e2a0a495f7466cb2e2f2ee2c300ab9','1e6b84723552416e9160ba51082727b1','ff8dc49e04304287ba28b34ca29d82d2',0),('b028bb4eb70544d699cf881a8cfe8246','42706fc39cee44ddbbe725d13a4c94d3','77961f4be1f845718669fc25268335e8',0),('b8d442cc4eb24a7fa92ed02231746503','42706fc39cee44ddbbe725d13a4c94d3','f3dbdfb0704c45cfa4f01a1028666b55',0),('c2bde92191d24623a6b9b29dec3a41ac','1e6b84723552416e9160ba51082727b1','980bb2107b034baf97bd22eb70171ce4',0),('d57e8d6bafff458f9c0e0d09da9af1a4','a4f3737150df495c9dc84aca4efd14b1','546f21bfe91646d69070a4e429b4380b',0),('de01ce25bffe4e93a1762f496f556e64','1e6b84723552416e9160ba51082727b1','81413ce6e2d14e54873d219ec8def861',0),('e04deedc2e1f499ab41ca3b6c7a9bfee','42706fc39cee44ddbbe725d13a4c94d3','a052991053e1467f9029a813e2ef68c6',0),('e1280efe2e3747d3af712e73ece05a2e','42706fc39cee44ddbbe725d13a4c94d3','0abdfd13d4704db6aedfe17657c901da',0),('e5d27d4f6a674fe8ae90bbc3b397fc27','42706fc39cee44ddbbe725d13a4c94d3','949d34a124c249ad8b8880ae406f50bf',0),('f30782b3423c4f0dbc019889adfabf5f','42706fc39cee44ddbbe725d13a4c94d3','2197ad03a32e4531b41cf90741247d15',0),('f8dd22368d034e35ba8466db2f86f98c','a4f3737150df495c9dc84aca4efd14b1','341090af00de488c924fa9ff7ff22579',0),('ff30a71b20634d43a996bb4f8dc018e1','a4f3737150df495c9dc84aca4efd14b1','2a1a8993555d413a80a7eec61c9d89a7',0);
/*!40000 ALTER TABLE `attendance_grade` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `attendance_type`
--

DROP TABLE IF EXISTS `attendance_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `attendance_type` (
  `id` varchar(32) NOT NULL,
  `name` varchar(60) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `attendance_type`
--

LOCK TABLES `attendance_type` WRITE;
/*!40000 ALTER TABLE `attendance_type` DISABLE KEYS */;
INSERT INTO `attendance_type` VALUES ('011a9f2fd59d4f61a98c40ee95a504e8','Лекция'),('8fc97247f8aa4f7c997a335326f15e73','Практика');
/*!40000 ALTER TABLE `attendance_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `grade`
--

DROP TABLE IF EXISTS `grade`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `grade` (
  `id` varchar(32) NOT NULL,
  `subject_id` varchar(32) NOT NULL,
  `date` datetime NOT NULL,
  `type_id` varchar(32) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `subject_id` (`subject_id`),
  KEY `type_id` (`type_id`),
  CONSTRAINT `grade_ibfk_1` FOREIGN KEY (`subject_id`) REFERENCES `subject` (`id`),
  CONSTRAINT `grade_ibfk_2` FOREIGN KEY (`type_id`) REFERENCES `type_grade` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `grade`
--

LOCK TABLES `grade` WRITE;
/*!40000 ALTER TABLE `grade` DISABLE KEYS */;
INSERT INTO `grade` VALUES ('8e1ca5aa9dad498d9c80a959aaaab874','c1cbaa20c7c14209b566e578bbbe8eb9','2021-12-21 00:00:00','b981914984da4935b406ded2c544a820'),('c18b25d34afa41d0bf3019aef5b6c124','b9ac28dfde2b4bc196a7f09154fe7fef','2021-12-20 00:00:00','693821cc8a5f494ebbcaf5550d28fb62'),('f3d78647ae7f4186b86e589a828b7028','c24d76414191419bbfe3a7eca6572262','2021-12-20 00:00:00','b981914984da4935b406ded2c544a820'),('fd09c62169ff473e9460ab2790c41725','b9ac28dfde2b4bc196a7f09154fe7fef','2021-12-21 00:00:00','b981914984da4935b406ded2c544a820');
/*!40000 ALTER TABLE `grade` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `grade_users`
--

DROP TABLE IF EXISTS `grade_users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `grade_users` (
  `id` varchar(32) NOT NULL,
  `user_id` varchar(32) NOT NULL,
  `grade_id` varchar(32) NOT NULL,
  `value` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `grade_id` (`grade_id`),
  CONSTRAINT `grade_users_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
  CONSTRAINT `grade_users_ibfk_2` FOREIGN KEY (`grade_id`) REFERENCES `grade` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `grade_users`
--

LOCK TABLES `grade_users` WRITE;
/*!40000 ALTER TABLE `grade_users` DISABLE KEYS */;
INSERT INTO `grade_users` VALUES ('b90584730b6946b4a6bc2a0cf7e13a9e','1e6b84723552416e9160ba51082727b1','c18b25d34afa41d0bf3019aef5b6c124',1),('cae234069c284939934cb7a3deafb9f2','42706fc39cee44ddbbe725d13a4c94d3','c18b25d34afa41d0bf3019aef5b6c124',1);
/*!40000 ALTER TABLE `grade_users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `group`
--

DROP TABLE IF EXISTS `group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `group` (
  `id` varchar(32) NOT NULL,
  `name` varchar(120) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `group`
--

LOCK TABLES `group` WRITE;
/*!40000 ALTER TABLE `group` DISABLE KEYS */;
INSERT INTO `group` VALUES ('0684cff744cd406ab9cd35e4d016063a','ИКТ-424'),('ad7ba7cc2ed6425c996426513b2c8bac','ИКТ-321');
/*!40000 ALTER TABLE `group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `lab`
--

DROP TABLE IF EXISTS `lab`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `lab` (
  `id` varchar(32) NOT NULL,
  `name` varchar(120) NOT NULL,
  `subject_id` varchar(32) NOT NULL,
  `datetime` datetime NOT NULL,
  `deadline` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `subject_id` (`subject_id`),
  CONSTRAINT `lab_ibfk_1` FOREIGN KEY (`subject_id`) REFERENCES `subject` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `lab`
--

LOCK TABLES `lab` WRITE;
/*!40000 ALTER TABLE `lab` DISABLE KEYS */;
INSERT INTO `lab` VALUES ('856bb7fb2dc244508e9d67c6f0e162b8','Создание системы сети и устройства телекоммуникации','c24d76414191419bbfe3a7eca6572262','2021-09-21 00:00:00','2021-09-28 23:59:59'),('9b144f9eadf743c2be793cb772dd677f','макет многосвязной линии передач','c1cbaa20c7c14209b566e578bbbe8eb9','2021-09-23 00:00:00','2021-09-30 23:59:59'),('d21e6f60bc804ed3883477fc5537ffd0','макет компьют. сети','b9ac28dfde2b4bc196a7f09154fe7fef','2021-09-20 00:00:00','2021-09-27 23:59:59');
/*!40000 ALTER TABLE `lab` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `labs_grade`
--

DROP TABLE IF EXISTS `labs_grade`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `labs_grade` (
  `id` varchar(32) NOT NULL,
  `lab_id` varchar(32) NOT NULL,
  `user_id` varchar(32) NOT NULL,
  `date` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `lab_id` (`lab_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `labs_grade_ibfk_1` FOREIGN KEY (`lab_id`) REFERENCES `lab` (`id`),
  CONSTRAINT `labs_grade_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `labs_grade`
--

LOCK TABLES `labs_grade` WRITE;
/*!40000 ALTER TABLE `labs_grade` DISABLE KEYS */;
INSERT INTO `labs_grade` VALUES ('44d01d5b6086403ca8fe1d99083c6808','d21e6f60bc804ed3883477fc5537ffd0','42706fc39cee44ddbbe725d13a4c94d3','2021-09-27 00:00:00'),('579cb29ae34f4594bc4eb79e824a28e2','d21e6f60bc804ed3883477fc5537ffd0','1e6b84723552416e9160ba51082727b1','2021-09-27 00:00:00'),('8e56edcadafe4a26acbc1c6db5002cc1','9b144f9eadf743c2be793cb772dd677f','a4f3737150df495c9dc84aca4efd14b1','2021-09-28 00:00:00'),('cb7fe2ebe9d844b8a4a003e6c86b6549','9b144f9eadf743c2be793cb772dd677f','1e6b84723552416e9160ba51082727b1','2021-09-30 00:00:00'),('cff944f887884483bd8d08600a64d0e5','d21e6f60bc804ed3883477fc5537ffd0','a4f3737150df495c9dc84aca4efd14b1','2021-09-25 00:00:00'),('e5d2ed20ac53449c8986130d2a1cc4fc','856bb7fb2dc244508e9d67c6f0e162b8','42706fc39cee44ddbbe725d13a4c94d3','2021-10-04 00:00:00'),('f6ba0594c6e1428789540534b8a105ca','d21e6f60bc804ed3883477fc5537ffd0','4f0cff74c5904d18b8e564f320ab7d97','2021-09-30 00:00:00');
/*!40000 ALTER TABLE `labs_grade` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rate_activity`
--

DROP TABLE IF EXISTS `rate_activity`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `rate_activity` (
  `id` varchar(32) NOT NULL,
  `activity_type_id` varchar(32) NOT NULL,
  `activity_sub_type_id` varchar(32) DEFAULT NULL,
  `value` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `activity_type_id` (`activity_type_id`),
  KEY `activity_sub_type_id` (`activity_sub_type_id`),
  CONSTRAINT `rate_activity_ibfk_1` FOREIGN KEY (`activity_type_id`) REFERENCES `activity_type` (`id`),
  CONSTRAINT `rate_activity_ibfk_2` FOREIGN KEY (`activity_sub_type_id`) REFERENCES `activity_sub_type` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rate_activity`
--

LOCK TABLES `rate_activity` WRITE;
/*!40000 ALTER TABLE `rate_activity` DISABLE KEYS */;
INSERT INTO `rate_activity` VALUES ('0d70848389ec4fffa7795d6b58cad1b8','d9af4dd7c72f419296478053dbc39afb','7d06d6b2e1694579a2582eec2ab8512b',2),('0e6ce7c8f63e48b6ab92426ffd818e4a','1f85fa98e0b04c69a3459c3f016b8c8a','7d06d6b2e1694579a2582eec2ab8512b',2),('2886366d88cb4b169c1e47a88812118b','1f85fa98e0b04c69a3459c3f016b8c8a','28396cc192494572802c680ce9aa4daa',2),('85e2f6dbf22747deb2fd6b208b8bf926','e7848cbb291b4327aa047e5b0f383da4',NULL,1),('8abffd087e7746adbc4b2daf52e8f8b4','d9af4dd7c72f419296478053dbc39afb','894c5a0cdd154d8d9de49a6352f625ec',1),('92764ad93dd64915aa3c640620fde86f','d9af4dd7c72f419296478053dbc39afb','28396cc192494572802c680ce9aa4daa',2),('9af07df629cc4853aaea1f320f70fcd4','080154b9ed8640fc8191a6fadd352a49',NULL,2),('c0f6056905724dcdba984a2cd72f5ab1','1f85fa98e0b04c69a3459c3f016b8c8a','894c5a0cdd154d8d9de49a6352f625ec',1);
/*!40000 ALTER TABLE `rate_activity` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `role`
--

DROP TABLE IF EXISTS `role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `role` (
  `id` varchar(32) NOT NULL,
  `name` varchar(20) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `role`
--

LOCK TABLES `role` WRITE;
/*!40000 ALTER TABLE `role` DISABLE KEYS */;
INSERT INTO `role` VALUES ('1090cfeca7b84ac483156a0c7fb15278','Преподаватель'),('1275694c4b1147239da3cba05c22dc75','Деканат'),('c35dcc2e5caf46f9868b27f470f574a2','Студент');
/*!40000 ALTER TABLE `role` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `subject`
--

DROP TABLE IF EXISTS `subject`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `subject` (
  `id` varchar(32) NOT NULL,
  `name` varchar(120) NOT NULL,
  `count_hours` int NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `subject`
--

LOCK TABLES `subject` WRITE;
/*!40000 ALTER TABLE `subject` DISABLE KEYS */;
INSERT INTO `subject` VALUES ('b9ac28dfde2b4bc196a7f09154fe7fef','Компьютерные сети',6),('c1cbaa20c7c14209b566e578bbbe8eb9','Многосвязные линии передач',6),('c24d76414191419bbfe3a7eca6572262','Системы сети и устройства телекоммуникации',6);
/*!40000 ALTER TABLE `subject` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `type_grade`
--

DROP TABLE IF EXISTS `type_grade`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `type_grade` (
  `id` varchar(32) NOT NULL,
  `name` varchar(60) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `type_grade`
--

LOCK TABLES `type_grade` WRITE;
/*!40000 ALTER TABLE `type_grade` DISABLE KEYS */;
INSERT INTO `type_grade` VALUES ('693821cc8a5f494ebbcaf5550d28fb62','Зачет'),('b981914984da4935b406ded2c544a820','Экзамен');
/*!40000 ALTER TABLE `type_grade` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `id` varchar(32) NOT NULL,
  `name` varchar(120) NOT NULL,
  `surname` varchar(120) NOT NULL,
  `patronymic` varchar(120) NOT NULL,
  `login` varchar(20) NOT NULL,
  `password` varchar(60) NOT NULL,
  `role_id` varchar(32) NOT NULL,
  `group_id` varchar(32) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `login` (`login`),
  KEY `role_id` (`role_id`),
  KEY `group_id` (`group_id`),
  CONSTRAINT `user_ibfk_1` FOREIGN KEY (`role_id`) REFERENCES `role` (`id`),
  CONSTRAINT `user_ibfk_2` FOREIGN KEY (`group_id`) REFERENCES `group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES ('1dfc8e41c0f1452b8607a3f9c7e92dc4','Юлия','Уразбахтина','Олеговна','urazbakhtina.yo','$2b$12$gkYxbbfH2917VwbZx4q3nOS9QMBqvkspY5yGh/0vYLKTbnUlSijV6','1275694c4b1147239da3cba05c22dc75',NULL),('1e6b84723552416e9160ba51082727b1','Алина','Ахкамова','Радиковна','ahkamova.ar','$2b$12$BDT.KcLLAfl1jV.yL0ZCw.WUFsvtWFhQnDETew9nQ3wVQajea6qCS','c35dcc2e5caf46f9868b27f470f574a2','0684cff744cd406ab9cd35e4d016063a'),('42706fc39cee44ddbbe725d13a4c94d3','Алексей','Шилов','Робертович','shilov.ar','$2b$12$rJ5Q9pUEigUAZ7Y5H6asgeRI3UYNandS0n74LpUxR7C8oQTCMkLNi','c35dcc2e5caf46f9868b27f470f574a2','ad7ba7cc2ed6425c996426513b2c8bac'),('4f0cff74c5904d18b8e564f320ab7d97','Ярослав','Павочкин','Константичнович','pavochkin.yk','$2b$12$.0WlsY8NB2PDIUZEhwVymOF1tTiI3pDo.6yjgjqZdBmwmwHapBTku','c35dcc2e5caf46f9868b27f470f574a2','ad7ba7cc2ed6425c996426513b2c8bac'),('565c1b9b40cb44a9a8370d282f9f29de','Руслан','Жданов','Римович','zhdanov.rr','$2b$12$q.4r26j/FVT1u11JhtrnEOJ/St1KnOV7hcdmZkD0Zx/Du06R9fEO2','1090cfeca7b84ac483156a0c7fb15278',NULL),('a4f3737150df495c9dc84aca4efd14b1','Элина','Яхина','Эльмаровна','yakhina.ee','$2b$12$dVSdpMj2aAuJRvtopgbT8.f3Kap7N98dKSM7mFaXQeqck2uMj4FVG','c35dcc2e5caf46f9868b27f470f574a2','0684cff744cd406ab9cd35e4d016063a');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-06-22 16:05:55
