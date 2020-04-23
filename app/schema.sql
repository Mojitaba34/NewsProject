-- Erfan Mosaddeghi
-- php my admin version 4.8.4
--
-- Host: 127.0.0.1
-- Generation Time: Apr 22, 2020 at 11:15 PM
-- Server version: 10.1.37-MariaDB
-- PHP Version: 7.3.0

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `newsdb`
--
CREATE DATABASE IF NOT EXISTS `newsdb` DEFAULT CHARACTER SET utf8 COLLATE utf8_persian_ci;
USE `newsdb`;

-- --------------------------------------------------------

--
-- Table structure for table `tbl_admin`
--

DROP TABLE IF EXISTS `tbl_admin`;
CREATE TABLE IF NOT EXISTS `tbl_admin` (
  `id_admin` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(30) COLLATE utf8_persian_ci DEFAULT NULL,
  `password` varchar(30) COLLATE utf8_persian_ci DEFAULT NULL,
  `email` varchar(40) COLLATE utf8_persian_ci DEFAULT NOT NULL,
  PRIMARY KEY (`id_admin`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_persian_ci;

-- --------------------------------------------------------

--
-- Table structure for table `tbl_news`
--

DROP TABLE IF EXISTS `tbl_news`;
CREATE TABLE IF NOT EXISTS `tbl_news` (
  `id_news` int(11) NOT NULL AUTO_INCREMENT,
  `news_title` text COLLATE utf8_persian_ci,
  `news_content` text COLLATE utf8_persian_ci,
  `news_link` text COLLATE utf8_persian_ci,
  `news_img_link` text COLLATE utf8_persian_ci,
  `news_date` date DEFAULT NULL,
  PRIMARY KEY (`id_news`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_persian_ci;

-- --------------------------------------------------------

--
-- Table structure for table `tbl_robots`
--

DROP TABLE IF EXISTS `tbl_robots`;
CREATE TABLE IF NOT EXISTS `tbl_robots` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `state_news_price` tinyint(1) NOT NULL,
  `state_crypto_price` tinyint(1) NOT NULL,
  `time_crawler` int(5) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_persian_ci;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
