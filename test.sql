-- MySQL dump 10.13  Distrib 5.5.46, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: web_db
-- ------------------------------------------------------
-- Server version	5.5.46-0ubuntu0.14.04.2

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Current Database: `web_db`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `web_db` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `web_db`;

--
-- Table structure for table `Album`
--

DROP TABLE IF EXISTS `Album`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Album` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `nomAlbum` varchar(30) NOT NULL,
  `nomArtist` varchar(30) NOT NULL,
  `Annee` year(4) DEFAULT NULL,
  `Label` smallint(5) unsigned DEFAULT NULL,
  `imagePath` varchar(120) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Album`
--

LOCK TABLES `Album` WRITE;
/*!40000 ALTER TABLE `Album` DISABLE KEYS */;
INSERT INTO `Album` (`nomAlbum`, `nomArtist`, `Annee`, `Label`, `imagePath`) VALUES ('XX','The xx',NULL,NULL,'/static/images/album/The xx/XX.jpg'),('Creatures','Rone',NULL,NULL,'/static/images/album/Rone/Creatures.jpg'),('All or Nothing','The Subways',NULL,NULL,'/static/images/album/The Subways/All or Nothing.jpg'),('Comme Des Enfants','Coeur De Pirate',NULL,NULL,'/static/images/album/Coeur De Pirate/Comme Des Enfants.jpg'),('Man on the Moon: The End of Da','Kid cudi',NULL,NULL,'/static/images/album/Kid cudi/Man on the Moon: The End of Day.jpg'),('Live in Hyde Park','Red Hot Chili Peppers',NULL,NULL,'/static/images/album/Red Hot Chili Peppers/Live in Hyde Park.jpg'),('Minutes to Midnight','Linkin Park',NULL,NULL,'/static/images/album/Linkin Park/Minutes to Midnight.jpg'),('Loco con da Frenchy Talkin','Shaka Ponk',NULL,NULL,'/static/images/album/Shaka Ponk/Loco con da Frenchy Talkin.jpg'),('Bad Porn Movie Trax','Shaka Ponk',NULL,NULL,'/static/images/album/Shaka Ponk/Bad Porn Movie Trax.jpg'),('Conditions','The Temper Trap',NULL,NULL,'/static/images/album/The Temper Trap/Conditions.jpg'),('We Started Nothing','The Ting Tings',NULL,NULL,'/static/images/album/The Ting Tings/We Started Nothing.jpg'),('Sweep of Days','Blue Foundation',NULL,NULL,'/static/images/album/Blue Foundation/Sweep of Days.jpg'),('Hybrid Theory','Linkin Park',NULL,NULL,'/static/images/album/Linkin Park/Hybrid Theory.jpg'),('How We Are','Bombay Bicycle Club',NULL,NULL,'/static/images/album/Bombay Bicycle Club/How We Are.jpg');
/*!40000 ALTER TABLE `Album` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Music`
--

DROP TABLE IF EXISTS `Music`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Music` (
  `idmusic` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `titre` varchar(120) DEFAULT NULL,
  `compositeur` varchar(60) DEFAULT NULL,
  `nomAlbum` varchar(30) NOT NULL,
  `annee` year(4) DEFAULT NULL,
  `label` varchar(30) DEFAULT NULL,
  `source` varchar(45) NOT NULL,
  `imagePath` longtext,
  `musicPath` longtext,
  `caract` longtext,
  `dateAjout` date DEFAULT NULL,
  PRIMARY KEY (`idmusic`)
) ENGINE=InnoDB AUTO_INCREMENT=68 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Music`
--

LOCK TABLES `Music` WRITE;
/*!40000 ALTER TABLE `Music` DISABLE KEYS */;
INSERT INTO `Music` VALUES (52,'Crystalised','The xx','XX',NULL,NULL,'local','/static/images/album/The xx/XX.jpg','/static/musiques/The xx/XX/Crystalised.mp3','truc','2015-05-30'),(53,'Intro','Rone','Creatures',NULL,NULL,'local','/static/images/album/Rone/Creatures.jpg','/static/musiques/Rone/Creatures/Intro.mp3','truc','2015-05-24'),(54,'Lost Boy','The Subways','All or Nothing',NULL,NULL,'local','/static/images/album/The Subways/All or Nothing.jpg','/static/musiques/The Subways/All or Nothing/Lost Boy.mp3','bidule','2015-05-24'),(55,'Comme Des Enfants','Coeur De Pirate','Comme Des Enfants',NULL,NULL,'local','/static/images/album/Coeur De Pirate/Comme Des Enfants.jpg','/static/musiques/Coeur De Pirate/Comme Des Enfants/Comme Des Enfants.mp3','pop','2015-05-25'),(56,'heart of lion','Kid cudi','Man on the Moon: The End of Da',NULL,NULL,'local','/static/images/album/Kid cudi/Man on the Moon: The End of Day.jpg','/static/musiques/Kid cudi/Man on the Moon: The End of Day/heart of lion.mp3','hip hop','2015-05-26'),(57,'Fortune Faded','Red Hot Chili Peppers','Live in Hyde Park',NULL,NULL,'local','/static/images/album/Red Hot Chili Peppers/Live in Hyde Park.jpg','/static/musiques/Red Hot Chili Peppers/Live in Hyde Park/Fortune Faded.mp3','alternatif','2015-05-26'),(58,'My December','Linkin Park','Hybrid Theory',NULL,NULL,'local','/static/images/album/Linkin Park/Hybrid Theory.jpg','/static/musiques/Linkin Park/Hybrid Theory/My December.mp3','punk','2015-05-26'),(59,'In The End','Linkin Park','Hybrid Theory',NULL,NULL,'local','/static/images/album/Linkin Park/Hybrid Theory.jpg','/static/musiques/Linkin Park/Hybrid Theory/In The End.mp3','punk','2015-05-29'),(60,'What I ve done','Linkin Park','Minutes to Midnight',NULL,NULL,'local','/static/images/album/Linkin Park/Minutes to Midnight.jpg','/static/musiques/Linkin Park/Minutes to Midnight/What I ve done.mp3','punk','2015-04-28'),(61,'Fonk me','Shaka Ponk','Loco con da Frenchy Talkin',NULL,NULL,'local','/static/images/album/Shaka Ponk/Loco con da Frenchy Talkin.jpg','/static/musiques/Shaka Ponk/Loco con da Frenchy Talkin/Fonk me.mp3','rock','2015-04-29'),(62,'French touch puta madre','Shaka Ponk','Bad Porn Movie Trax',NULL,NULL,'local','/static/images/album/Shaka Ponk/Bad Porn Movie Trax.jpg','/static/musiques/Shaka Ponk/Bad Porn Movie Trax/French touch puta madre.mp3','rock','2015-04-30'),(63,'Science Of Fear','The Temper Trap','Conditions',NULL,NULL,'local','/static/images/album/The Temper Trap/Conditions.jpg','/static/musiques/The Temper Trap/Conditions/Science Of Fear.mp3','rock','2015-05-10'),(64,'We Walk','The Ting Tings','We Started Nothing',NULL,NULL,'local','/static/images/album/The Ting Tings/We Started Nothing.jpg','/static/musiques/The Ting Tings/We Started Nothing/We Walk.mp3','cool','2015-05-10'),(65,'Bonfires','Blue Foundation','Sweep of Days',NULL,NULL,'local','/static/images/album/Blue Foundation/Sweep of Days.jpg','/static/musiques/Blue Foundation/Sweep of Days/Bonfires.mp3','salut','2015-05-16'),(66,'How Are We','Bombay Bicycle Club','How We Are',NULL,NULL,'local','/static/images/album/Bombay Bicycle Club/How We Are.jpg','/static/musiques/Bombay Bicycle Club/How We Are/How Are We.mp3','indien','2015-05-16'),(67,'Ghost','Bombay Bicycle Club','How We Are',NULL,NULL,'local','/static/images/album/Bombay Bicycle Club/How We Are.jpg','/static/musiques/Bombay Bicycle Club/How We Are/Ghost.mp3','indien','2015-05-30');
/*!40000 ALTER TABLE `Music` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `avis`
--

DROP TABLE IF EXISTS `avis`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `avis` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `useremail` varchar(30) NOT NULL,
  `idmusic` int(10) unsigned NOT NULL,
  `note` smallint(5) unsigned DEFAULT NULL,
  `humeur` longtext,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `avis`
--

LOCK TABLES `avis` WRITE;
/*!40000 ALTER TABLE `avis` DISABLE KEYS */;
INSERT INTO `avis` VALUES (7,'lukatoni1992@gmail.com',52,5,'Cool'),(8,'lukatoni1992@gmail.com',65,3,'Cool'),(9,'lukatoni1992@gmail.com',56,3,'Cool'),(10,'foo@example.com',52,2,'Codeur'),(11,'foo@example.com',53,4,NULL),(12,'foo@example.com',54,5,NULL),(13,'foo@example.com',55,5,NULL),(14,'foo@example.com',56,3,NULL),(15,'foo@example.com',57,2,NULL),(16,'foo@example.com',58,1,NULL),(17,'foo@example.com',60,2,NULL),(18,'foo@example.com',61,4,NULL),(19,'foo@example.com',62,5,NULL),(20,'foo@example.com',63,4,NULL),(21,'foo@example.com',64,2,NULL),(22,'foo@example.com',67,3,NULL),(23,'foo@example.com',66,4,NULL),(24,'a@b.com',52,5,'Calme'),(25,'lukatoni1992@gmail.com',1,NULL,'Gaming'),(26,'lukatoni1992@gmail.com',16,NULL,'Chill'),(27,'lukatoni1992@gmail.com',53,4,'Motivee'),(28,'lukatoni1992@gmail.com',54,4,'Motivee'),(29,'celine@example.com',53,5,'Creative'),(30,'celine@example.com',52,4,'Triste'),(31,'me@example.com',54,5,'Triste'),(32,'me@example.com',56,5,'Chill');
/*!40000 ALTER TABLE `avis` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `musiques`
--

DROP TABLE IF EXISTS `musiques`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `musiques` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `titre` varchar(30) DEFAULT NULL,
  `compositeur` varchar(60) DEFAULT NULL,
  `album` varchar(60) DEFAULT NULL,
  `annee` year(4) DEFAULT NULL,
  `label` varchar(30) DEFAULT NULL,
  `imagePath` longtext,
  `musicPath` longtext,
  `caracteristiques` longtext,
  `dateAjout` date DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=68 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `musiques`
--

LOCK TABLES `musiques` WRITE;
/*!40000 ALTER TABLE `musiques` DISABLE KEYS */;
INSERT INTO `musiques` VALUES (52,'Crystalised','The xx','XX',NULL,NULL,'/static/images/album/The xx/XX.jpg','/static/musiques/The xx/XX/Crystalised.mp3','truc','2015-05-30'),(53,'Intro','Rone','Creatures',NULL,NULL,'/static/images/album/Rone/Creatures.jpg','/static/musiques/Rone/Creatures/Intro.mp3','truc','2015-05-24'),(54,'Lost Boy','The Subways','All or Nothing',NULL,NULL,'/static/images/album/The Subways/All or Nothing.jpg','/static/musiques/The Subways/All or Nothing/Lost Boy.mp3','bidule','2015-05-24'),(55,'Comme Des Enfants','Coeur De Pirate','Comme Des Enfants',NULL,NULL,'/static/images/album/Coeur De Pirate/Comme Des Enfants.jpg','/static/musiques/Coeur De Pirate/Comme Des Enfants/Comme Des Enfants.mp3','pop','2015-05-25'),(56,'heart of lion','Kid cudi','Man on the Moon: The End of Day',NULL,NULL,'/static/images/album/Kid cudi/Man on the Moon: The End of Day.jpg','/static/musiques/Kid cudi/Man on the Moon: The End of Day/heart of lion.mp3','hip hop','2015-05-26'),(57,'Fortune Faded','Red Hot Chili Peppers','Live in Hyde Park',NULL,NULL,'/static/images/album/Red Hot Chili Peppers/Live in Hyde Park.jpg','/static/musiques/Red Hot Chili Peppers/Live in Hyde Park/Fortune Faded.mp3','alternatif','2015-05-26'),(58,'My December','Linkin Park','Hybrid Theory',NULL,NULL,'/static/images/album/Linkin Park/Hybrid Theory.jpg','/static/musiques/Linkin Park/Hybrid Theory/My December.mp3','punk','2015-05-26'),(59,'In The End','Linkin Park','Hybrid Theory',NULL,NULL,'/static/images/album/Linkin Park/Hybrid Theory.jpg','/static/musiques/Linkin Park/Hybrid Theory/In The End.mp3','punk','2015-05-29'),(60,'What I ve done','Linkin Park','Minutes to Midnight',NULL,NULL,'/static/images/album/Linkin Park/Minutes to Midnight.jpg','/static/musiques/Linkin Park/Minutes to Midnight/What I ve done.mp3','punk','2015-04-28'),(61,'Fonk me','Shaka Ponk','Loco con da Frenchy Talkin',NULL,NULL,'/static/images/album/Shaka Ponk/Loco con da Frenchy Talkin.jpg','/static/musiques/Shaka Ponk/Loco con da Frenchy Talkin/Fonk me.mp3','rock','2015-04-29'),(62,'French touch puta madre','Shaka Ponk','Bad Porn Movie Trax',NULL,NULL,'/static/images/album/Shaka Ponk/Bad Porn Movie Trax.jpg','/static/musiques/Shaka Ponk/Bad Porn Movie Trax/French touch puta madre.mp3','rock','2015-04-30'),(63,'Science Of Fear','The Temper Trap','Conditions',NULL,NULL,'/static/images/album/The Temper Trap/Conditions.jpg','/static/musiques/The Temper Trap/Conditions/Science Of Fear.mp3','rock','2015-05-10'),(64,'We Walk','The Ting Tings','We Started Nothing',NULL,NULL,'/static/images/album/The Ting Tings/We Started Nothing.jpg','/static/musiques/The Ting Tings/We Started Nothing/We Walk.mp3','cool','2015-05-10'),(65,'Bonfires','Blue Foundation','Sweep of Days',NULL,NULL,'/static/images/album/Blue Foundation/Sweep of Days.jpg','/static/musiques/Blue Foundation/Sweep of Days/Bonfires.mp3','salut','2015-05-16'),(66,'How Are We','Bombay Bicycle Club','How We Are',NULL,NULL,'/static/images/album/Bombay Bicycle Club/How We Are.jpg','/static/musiques/Bombay Bicycle Club/How We Are/How Are We.mp3','indien','2015-05-16'),(67,'Ghost','Bombay Bicycle Club','How We Are',NULL,NULL,'/static/images/album/Bombay Bicycle Club/How We Are.jpg','/static/musiques/Bombay Bicycle Club/How We Are/Ghost.mp3','indien','2015-05-30');
/*!40000 ALTER TABLE `musiques` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `email` varchar(30) NOT NULL,
  `password` varchar(120) NOT NULL,
  `pseudo` varchar(30) DEFAULT NULL,
  `imagePath` varchar(2083) DEFAULT NULL,
  PRIMARY KEY (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES ('celine@example.com','lok','céline',NULL),('foo@example.com','1234',NULL,NULL),('lukatoni192@gmail.com','lok','kjhb',NULL),('lukatoni1992112@gmail.com','lok','kksksks',NULL),('lukatoni199212@gmail.com','lok3','AMINE',NULL),('lukatoni19922@gmail.com','lok','jsncjnc',NULL),('lukatoni1992878@gmail.com','lok','aelf,zknzlf',NULL),('lukatoni1992@gmail.com','lok','lokmane','/static/images/userprofile/lukatoni1992@gmail.com.jpg'),('me@example.com','lok','example',NULL);
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

-- Dump completed on 2015-11-17 17:19:51
