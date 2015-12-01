CREATE DATABASE  IF NOT EXISTS `web_db` /*!40100 DEFAULT CHARACTER SET utf8 */;
USE `web_db`;
-- MySQL dump 10.13  Distrib 5.6.23, for Win64 (x86_64)
--
-- Host: localhost    Database: web_db
-- ------------------------------------------------------
-- Server version	5.6.24-log

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
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `avis`
--

LOCK TABLES `avis` WRITE;
/*!40000 ALTER TABLE `avis` DISABLE KEYS */;
INSERT INTO `avis` VALUES (7,'lukatoni1992@gmail.com',52,5,'Cool'),(8,'lukatoni1992@gmail.com',65,3,'Cool'),(9,'lukatoni1992@gmail.com',56,3,'Cool'),(10,'foo@example.com',52,2,'Codeur'),(11,'foo@example.com',53,4,NULL),(12,'foo@example.com',54,5,NULL),(13,'foo@example.com',55,5,NULL),(14,'foo@example.com',56,3,NULL),(15,'foo@example.com',57,2,NULL),(16,'foo@example.com',58,1,NULL),(17,'foo@example.com',60,2,NULL),(18,'foo@example.com',61,4,NULL),(19,'foo@example.com',62,5,NULL),(20,'foo@example.com',63,4,NULL),(21,'foo@example.com',64,2,NULL),(22,'foo@example.com',67,3,NULL),(23,'foo@example.com',66,4,NULL),(24,'a@b.com',52,5,'Calme'),(25,'lukatoni1992@gmail.com',1,NULL,'Gaming'),(26,'lukatoni1992@gmail.com',16,NULL,'Chill'),(27,'lukatoni1992@gmail.com',53,4,'Motivee'),(28,'lukatoni1992@gmail.com',54,4,'Motivee'),(29,'celine@example.com',53,5,'Creative'),(30,'celine@example.com',52,4,'Triste'),(31,'me@example.com',54,5,'Triste'),(32,'me@example.com',56,5,'Chill'),(33,'asd@example.com',52,3,'Chill'),(34,'asd@example.com',118,4,NULL);
/*!40000 ALTER TABLE `avis` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `music`
--

DROP TABLE IF EXISTS `music`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `music` (
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
) ENGINE=InnoDB AUTO_INCREMENT=168 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `music`
--

LOCK TABLES `music` WRITE;
/*!40000 ALTER TABLE `music` DISABLE KEYS */;
INSERT INTO `music` VALUES (52,'Crystalised','The xx','XX',NULL,NULL,'local','/static/images/album/The xx/XX.jpg','/static/musiques/The xx/XX/Crystalised.mp3','truc','2015-05-30'),(53,'Intro','Rone','Creatures',NULL,NULL,'local','/static/images/album/Rone/Creatures.jpg','/static/musiques/Rone/Creatures/Intro.mp3','truc','2015-05-24'),(54,'Lost Boy','The Subways','All or Nothing',NULL,NULL,'local','/static/images/album/The Subways/All or Nothing.jpg','/static/musiques/The Subways/All or Nothing/Lost Boy.mp3','bidule','2015-05-24'),(55,'Comme Des Enfants','Coeur De Pirate','Comme Des Enfants',NULL,NULL,'local','/static/images/album/Coeur De Pirate/Comme Des Enfants.jpg','/static/musiques/Coeur De Pirate/Comme Des Enfants/Comme Des Enfants.mp3','pop','2015-05-25'),(56,'heart of lion','Kid cudi','Man on the Moon: The End of Da',NULL,NULL,'local','/static/images/album/Kid cudi/Man on the Moon: The End of Day.jpg','/static/musiques/Kid cudi/Man on the Moon: The End of Day/heart of lion.mp3','hip hop','2015-05-26'),(57,'Fortune Faded','Red Hot Chili Peppers','Live in Hyde Park',NULL,NULL,'local','/static/images/album/Red Hot Chili Peppers/Live in Hyde Park.jpg','/static/musiques/Red Hot Chili Peppers/Live in Hyde Park/Fortune Faded.mp3','alternatif','2015-05-26'),(58,'My December','Linkin Park','Hybrid Theory',NULL,NULL,'local','/static/images/album/Linkin Park/Hybrid Theory.jpg','/static/musiques/Linkin Park/Hybrid Theory/My December.mp3','punk','2015-05-26'),(59,'In The End','Linkin Park','Hybrid Theory',NULL,NULL,'local','/static/images/album/Linkin Park/Hybrid Theory.jpg','/static/musiques/Linkin Park/Hybrid Theory/In The End.mp3','punk','2015-05-29'),(60,'What I ve done','Linkin Park','Minutes to Midnight',NULL,NULL,'local','/static/images/album/Linkin Park/Minutes to Midnight.jpg','/static/musiques/Linkin Park/Minutes to Midnight/What I ve done.mp3','punk','2015-04-28'),(61,'Fonk me','Shaka Ponk','Loco con da Frenchy Talkin',NULL,NULL,'local','/static/images/album/Shaka Ponk/Loco con da Frenchy Talkin.jpg','/static/musiques/Shaka Ponk/Loco con da Frenchy Talkin/Fonk me.mp3','rock','2015-04-29'),(62,'French touch puta madre','Shaka Ponk','Bad Porn Movie Trax',NULL,NULL,'local','/static/images/album/Shaka Ponk/Bad Porn Movie Trax.jpg','/static/musiques/Shaka Ponk/Bad Porn Movie Trax/French touch puta madre.mp3','rock','2015-04-30'),(63,'Science Of Fear','The Temper Trap','Conditions',NULL,NULL,'local','/static/images/album/The Temper Trap/Conditions.jpg','/static/musiques/The Temper Trap/Conditions/Science Of Fear.mp3','rock','2015-05-10'),(64,'We Walk','The Ting Tings','We Started Nothing',NULL,NULL,'local','/static/images/album/The Ting Tings/We Started Nothing.jpg','/static/musiques/The Ting Tings/We Started Nothing/We Walk.mp3','cool','2015-05-10'),(65,'Bonfires','Blue Foundation','Sweep of Days',NULL,NULL,'local','/static/images/album/Blue Foundation/Sweep of Days.jpg','/static/musiques/Blue Foundation/Sweep of Days/Bonfires.mp3','salut','2015-05-16'),(66,'How Are We','Bombay Bicycle Club','How We Are',NULL,NULL,'local','/static/images/album/Bombay Bicycle Club/How We Are.jpg','/static/musiques/Bombay Bicycle Club/How We Are/How Are We.mp3','indien','2015-05-16'),(67,'Ghost','Bombay Bicycle Club','How We Are',NULL,NULL,'local','/static/images/album/Bombay Bicycle Club/How We Are.jpg','/static/musiques/Bombay Bicycle Club/How We Are/Ghost.mp3','indien','2015-05-30'),(118,'Roar (Official)','Katy Perry','Unkown',NULL,NULL,'youtube',NULL,'CevxZvSJLk8',NULL,'2015-11-26'),(119,'Wake Me Up (Official Video)','Avicii','Unkown',NULL,NULL,'youtube',NULL,'IcrbM1l_BoI',NULL,'2015-11-26'),(120,'Royals (US Version)','Lorde','Unkown',NULL,NULL,'youtube',NULL,'nlcIKh6sBtc',NULL,'2015-11-26'),(121,'Wrecking Ball','Miley Cyrus','Unkown',NULL,NULL,'youtube',NULL,'My2FRPA3Gf8',NULL,'2015-11-26'),(122,'La La La ft. Sam Smith','Naughty Boy','Unkown',NULL,NULL,'youtube',NULL,'3O1_3zBUKM8',NULL,'2015-11-26'),(123,'Dark Horse (Official) ft. Juicy J','Katy Perry','Unkown',NULL,NULL,'youtube',NULL,'0KSOMA3QBU0',NULL,'2015-11-26'),(124,'Counting Stars','OneRepublic','Unkown',NULL,NULL,'youtube',NULL,'hT_nvWreIhg',NULL,'2015-11-26'),(125,'The Monster (Explicit) ft. Rihanna','Eminem','Unkown',NULL,NULL,'youtube',NULL,'EHkozMIXZ8w',NULL,'2015-11-26'),(126,'Beauty And A Beat ft. Nicki Minaj','Justin Bieber','Unkown',NULL,NULL,'youtube',NULL,'Ys7-6_t7OEQ',NULL,'2015-11-26'),(127,'Firework','Katy Perry','Unkown',NULL,NULL,'youtube',NULL,'QGJuMBdaqIw',NULL,'2015-11-26'),(128,'Party Rock Anthem ft. Lauren Bennett, GoonRock','LMFAO','Unkown',NULL,NULL,'youtube',NULL,'KQ6zr6kCPj8',NULL,'2015-11-26'),(129,'Not Afraid','Eminem','Unkown',NULL,NULL,'youtube',NULL,'j5-yKhDd64s',NULL,'2015-11-26'),(130,'Only Girl (In The World)','Rihanna','Unkown',NULL,NULL,'youtube',NULL,'pa14VNsdSYM',NULL,'2015-11-26'),(131,'Love The Way You Lie ft. Rihanna','Eminem','Unkown',NULL,NULL,'youtube',NULL,'uelHwf8o7_U',NULL,'2015-11-26'),(132,'Burn','Ellie Goulding','Unkown',NULL,NULL,'youtube',NULL,'CGyEd0aKWZE',NULL,'2015-11-26'),(133,'Diamonds','Rihanna','Unkown',NULL,NULL,'youtube',NULL,'lWA2pjMjpBs',NULL,'2015-11-26'),(134,'Someone Like You','Adele','Unkown',NULL,NULL,'youtube',NULL,'hLQl3WQQoQ0',NULL,'2015-11-26'),(135,'Feel This Moment ft. Christina Aguilera','Pitbull','Unkown',NULL,NULL,'youtube',NULL,'5jlI4uzZGjU',NULL,'2015-11-26'),(136,'Never Say Never ft. Jaden Smith','Justin Bieber','Unkown',NULL,NULL,'youtube',NULL,'_Z5-P9v3F8w',NULL,'2015-11-26'),(137,'Scream & Shout ft. Britney Spears','will.i.am','Unkown',NULL,NULL,'youtube',NULL,'kYtGl1dX5qI',NULL,'2015-11-26'),(138,'Bad Romance','Lady Gaga','Unkown',NULL,NULL,'youtube',NULL,'qrO4YZeyl0I',NULL,'2015-11-26'),(139,'Timber ft. Ke$ha','Pitbull','Unkown',NULL,NULL,'youtube',NULL,'hHUbLv4ThOo',NULL,'2015-11-26'),(140,'Super Bass','Nicki Minaj','Unkown',NULL,NULL,'youtube',NULL,'4JipHEz53sU',NULL,'2015-11-26'),(141,'We Found Love ft. Calvin Harris','Rihanna','Unkown',NULL,NULL,'youtube',NULL,'tg00YEETFzg',NULL,'2015-11-26'),(142,'International Love ft. Chris Brown','Pitbull','Unkown',NULL,NULL,'youtube',NULL,'CdXesX6mYUE',NULL,'2015-11-26'),(143,'Levels','Avicii','Unkown',NULL,NULL,'youtube',NULL,'_ovdm2yX4MA',NULL,'2015-11-26'),(144,'On The Floor ft. Pitbull','Jennifer Lopez','Unkown',NULL,NULL,'youtube',NULL,'t4H_Zoh7G5A',NULL,'2015-11-26'),(145,'What Makes You Beautiful','One Direction','Unkown',NULL,NULL,'youtube',NULL,'QJO3ROT-A4E',NULL,'2015-11-26'),(146,'Waka Waka (This Time for Africa) (The Official 2010 FIFA World Cup™ Song)','Shakira','Unkown',NULL,NULL,'youtube',NULL,'pRpeEdMmmQ0',NULL,'2015-11-26'),(147,'Rain Over Me ft. Marc Anthony','Pitbull','Unkown',NULL,NULL,'youtube',NULL,'SmM0653YvXU',NULL,'2015-11-26'),(148,'Rolling in the Deep','Adele','Unkown',NULL,NULL,'youtube',NULL,'rYEDA3JcQqw',NULL,'2015-11-26'),(149,'Can\'t Remember to Forget You ft. Rihanna','Shakira','Unkown',NULL,NULL,'youtube',NULL,'o3mP3mJDL2k',NULL,'2015-11-26'),(150,'Summer','Calvin Harris','Unkown',NULL,NULL,'youtube',NULL,'ebXbLfLACGM',NULL,'2015-11-26'),(151,'What\'s My Name? ft. Drake','Rihanna','Unkown',NULL,NULL,'youtube',NULL,'U0CGsw6h60k',NULL,'2015-11-26'),(152,'Just Dance ft. Colby O\'Donis','Lady Gaga','Unkown',NULL,NULL,'youtube',NULL,'2Abk1jAONjw',NULL,'2015-11-26'),(153,'Single Ladies (Put a Ring on It)','Beyoncé','Unkown',NULL,NULL,'youtube',NULL,'4m1EFMoRFvY',NULL,'2015-11-26'),(154,'Price Tag ft. B.o.B','Jessie J','Unkown',NULL,NULL,'youtube',NULL,'qMxX-QOV9tI',NULL,'2015-11-26'),(155,'You Belong With Me','Taylor Swift','Unkown',NULL,NULL,'youtube',NULL,'VuNIsY6JdUw',NULL,'2015-11-26'),(156,'TiK ToK','Ke$ha','Unkown',NULL,NULL,'youtube',NULL,'iP6XpLQM2Cs',NULL,'2015-11-26'),(157,'Bailando (Español) ft. Descemer Bueno, Gente De Zona','Enrique Iglesias','Unkown',NULL,NULL,'youtube',NULL,'NUsoVlDFqZg',NULL,'2015-11-26'),(158,'Shake It Off','Taylor Swift','Unkown',NULL,NULL,'youtube',NULL,'nfWlot6h_JM',NULL,'2015-11-26'),(159,'All About That Bass','Meghan Trainor','Unkown',NULL,NULL,'youtube',NULL,'7PCkvCPvDXk',NULL,'2015-11-26'),(160,'See You Again ft. Charlie Puth [Official Video] Furious 7 Soundtrack','Wiz Khalifa','Unkown',NULL,NULL,'youtube',NULL,'RgKAFK5djSk',NULL,'2015-11-26'),(161,'Blank Space','Taylor Swift','Unkown',NULL,NULL,'youtube',NULL,'e-ORhEE9VVg',NULL,'2015-11-26'),(162,'Chandelier (Official Video)','Sia','Unkown',NULL,NULL,'youtube',NULL,'2vjPBrBU-TM',NULL,'2015-11-26'),(163,'Baby ft. Ludacris','Justin Bieber','Unkown',NULL,NULL,'youtube',NULL,'kffacxfA7G4',NULL,'2015-11-26'),(164,'Uptown Funk ft. Bruno Mars','Mark Ronson','Unkown',NULL,NULL,'youtube',NULL,'OPf0YbXqDm0',NULL,'2015-11-26'),(165,'Bad Blood ft. Kendrick Lamar','Taylor Swift','Unkown',NULL,NULL,'youtube',NULL,'QcIy9NiNbmo',NULL,'2015-11-26'),(166,'Sugar','Maroon 5','Unkown',NULL,NULL,'youtube',NULL,'09R8_2nJtjg',NULL,'2015-11-26'),(167,'Hips Don\'t Lie ft. Wyclef Jean','Shakira','Unkown',NULL,NULL,'youtube',NULL,'DUT5rEU6pqM',NULL,'2015-11-26');
/*!40000 ALTER TABLE `music` ENABLE KEYS */;
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
INSERT INTO `users` VALUES ('asd@example.com','cda1d665441ef8120c3d3e82610e74ab0d3b043763784676654d8ef1','asd',NULL),('celine@example.com','lok','céline',NULL),('ed@example.com','23970774a854b7f7cb4dcab703406688dad7e58979400ba13b9f8963','edmundo',NULL),('foo@example.com','1234',NULL,NULL),('lukatoni192@gmail.com','lok','kjhb',NULL),('lukatoni1992112@gmail.com','lok','kksksks',NULL),('lukatoni199212@gmail.com','lok3','AMINE',NULL),('lukatoni19922@gmail.com','lok','jsncjnc',NULL),('lukatoni1992878@gmail.com','lok','aelf,zknzlf',NULL),('lukatoni1992@gmail.com','lok','lokmane','/static/images/userprofile/lukatoni1992@gmail.com.jpg'),('me@example.com','lok','example',NULL);
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

-- Dump completed on 2015-12-01 15:15:49
