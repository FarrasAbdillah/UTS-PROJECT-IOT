-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               8.0.30 - MySQL Community Server - GPL
-- Server OS:                    Win64
-- HeidiSQL Version:             12.1.0.6537
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Dumping database structure for uts_pem_iot
DROP DATABASE IF EXISTS `uts_pem_iot`;
CREATE DATABASE IF NOT EXISTS `uts_pem_iot` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `uts_pem_iot`;

-- Dumping structure for table uts_pem_iot.data_sensor
DROP TABLE IF EXISTS `data_sensor`;
CREATE TABLE IF NOT EXISTS `data_sensor` (
  `id` int NOT NULL AUTO_INCREMENT,
  `suhu` float DEFAULT NULL,
  `humidity` float DEFAULT NULL,
  `lux` float DEFAULT NULL,
  `timestamp` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=254 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table uts_pem_iot.data_sensor: ~6 rows (approximately)
INSERT INTO `data_sensor` (`id`, `suhu`, `humidity`, `lux`, `timestamp`) VALUES
	(248, 24, 40, 244, '2025-11-10 12:52:59'),
	(249, 24, 40, 244, '2025-11-10 13:27:59'),
	(250, 24, 40, 244, '2025-11-10 13:29:02'),
	(251, 24, 40, 244, '2025-11-10 13:35:09'),
	(252, 24, 40, 244, '2025-11-10 13:48:25'),
	(253, 24, 40, 244, '2025-11-11 02:10:04');

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
