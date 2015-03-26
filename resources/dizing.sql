-- phpMyAdmin SQL Dump
-- version 4.2.6deb1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Mar 20, 2015 at 03:53 PM
-- Server version: 5.5.40-0ubuntu1
-- PHP Version: 5.5.12-2ubuntu4.1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `dizing`
--

-- --------------------------------------------------------

--
-- Table structure for table `analyzed`
--

CREATE TABLE IF NOT EXISTS `analyzed` (
`w_id` int(11) NOT NULL,
  `original` varchar(64) COLLATE utf8_turkish_ci NOT NULL,
  `pos` varchar(64) COLLATE utf8_turkish_ci NOT NULL,
  `stem1` varchar(64) COLLATE utf8_turkish_ci NOT NULL,
  `stem2` varchar(64) COLLATE utf8_turkish_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `film`
--

CREATE TABLE IF NOT EXISTS `film` (
  `title` varchar(64) COLLATE utf8_turkish_ci NOT NULL,
  `path_scene` varchar(100) COLLATE utf8_turkish_ci NOT NULL,
`f_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `scene`
--

CREATE TABLE IF NOT EXISTS `scene` (
`s_id` int(20) NOT NULL,
  `path_scene` varchar(1000) COLLATE utf8_turkish_ci DEFAULT NULL,
  `sentence` text COLLATE utf8_turkish_ci NOT NULL,
  `start` varchar(16) COLLATE utf8_turkish_ci NOT NULL,
  `stop` varchar(16) COLLATE utf8_turkish_ci NOT NULL,
  `clip_file` varchar(1000) COLLATE utf8_turkish_ci DEFAULT NULL,
  `word` varchar(32) COLLATE utf8_turkish_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci AUTO_INCREMENT=1 ;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `analyzed`
--
ALTER TABLE `analyzed`
 ADD PRIMARY KEY (`w_id`);

--
-- Indexes for table `film`
--
ALTER TABLE `film`
 ADD PRIMARY KEY (`f_id`);

--
-- Indexes for table `scene`
--
ALTER TABLE `scene`
 ADD PRIMARY KEY (`s_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `analyzed`
--
ALTER TABLE `analyzed`
MODIFY `w_id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `film`
--
ALTER TABLE `film`
MODIFY `f_id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `scene`
--
ALTER TABLE `scene`
MODIFY `s_id` int(20) NOT NULL AUTO_INCREMENT;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
