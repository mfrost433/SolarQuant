-- phpMyAdmin SQL Dump
-- version 4.5.4.1deb2ubuntu2
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Jul 11, 2018 at 04:57 PM
-- Server version: 5.7.22-0ubuntu0.16.04.1
-- PHP Version: 7.0.28-0ubuntu0.16.04.1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `solarquant`
--

-- --------------------------------------------------------

--
-- Table structure for table `analysis_engine`
--

CREATE TABLE `analysis_engine` (
  `analysis_engine_id` int(11) NOT NULL,
  `analysis_engine_description` varchar(255) NOT NULL,
  `analysis_engine_code` varchar(20) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `node_datum`
--

CREATE TABLE `node_datum` (
  `NODE_ID` int(11) NOT NULL,
  `SOURCE_ID` varchar(20) NOT NULL,
  `DATE_CREATED` datetime NOT NULL,
  `WATT_HOURS` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `node_source`
--

CREATE TABLE `node_source` (
  `node_id` int(11) NOT NULL,
  `sourceId` varchar(255) NOT NULL,
  `source_type_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `owm_data`
--

CREATE TABLE `owm_data` (
  `DATE_CREATED` datetime NOT NULL,
  `TEMP` float NOT NULL,
  `WIND_DIRECTION` float NOT NULL,
  `WIND_SPEED` float NOT NULL,
  `CLOUDINESS` float NOT NULL,
  `PRESSURE` float NOT NULL,
  `HUMIDITY` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `prediction_input`
--

CREATE TABLE `prediction_input` (
  `NODE_ID` int(11) NOT NULL,
  `SOURCE_ID` varchar(20) NOT NULL,
  `DATE_PREDICTING` datetime NOT NULL,
  `ENTRY_DATE` datetime NOT NULL,
  `PREV_WEEK_WATTHOURS` float NOT NULL,
  `PREV_2WEEK_WATTHOURS` float NOT NULL,
  `PRESSURE` float NOT NULL,
  `HUMIDITY` float NOT NULL,
  `TEMP` float NOT NULL,
  `CLOUDINESS` float NOT NULL,
  `WIND_SPEED` float NOT NULL,
  `WIND_DIR` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `prediction_output`
--

CREATE TABLE `prediction_output` (
  `REQUEST_ID` int(11) NOT NULL,
  `PREDICTED_WATT_HOURS` float NOT NULL,
  `WATT_HOURS` float DEFAULT NULL,
  `DATE` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `prediction_requests`
--

CREATE TABLE `prediction_requests` (
  `REQUEST_ID` int(11) NOT NULL,
  `NAME` varchar(10) DEFAULT NULL,
  `NODE_ID` int(11) NOT NULL,
  `SOURCE_ID` varchar(20) NOT NULL,
  `DATE_REQUESTED` datetime NOT NULL,
  `STATUS` int(11) NOT NULL,
  `REQUEST_ENGINE` varchar(20) NOT NULL,
  `START_DATE` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `DYNAMIC` tinyint(1) NOT NULL DEFAULT '0',
  `END_DATE` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `prediction_state_time`
--

CREATE TABLE `prediction_state_time` (
  `REQUEST_ID` int(11) NOT NULL,
  `STATE` int(11) NOT NULL,
  `START_DATE` datetime NOT NULL,
  `COMPLETION_DATE` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `registered_nodes`
--

CREATE TABLE `registered_nodes` (
  `NODE_ID` int(11) NOT NULL,
  `NODE_TYPE` int(11) NOT NULL,
  `LOCATION` varchar(20) NOT NULL,
  `TIMEZONE` varchar(20) NOT NULL,
  `CITY` varchar(20) NOT NULL,
  `COUNTRY` varchar(20) NOT NULL,
  `NOTES` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `requests`
--

CREATE TABLE `requests` (
  `REQUEST_ID` int(11) NOT NULL,
  `NODE_ID` int(11) NOT NULL,
  `SOURCE_ID` varchar(20) NOT NULL,
  `DATE_REQUESTED` datetime NOT NULL,
  `STATUS` int(11) NOT NULL,
  `REQUEST_ENGINE` varchar(20) NOT NULL,
  `REQUEST_TYPE` varchar(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `trained_models`
--

CREATE TABLE `trained_models` (
  `NODE_ID` int(11) NOT NULL,
  `SOURCE_ID` varchar(50) NOT NULL,
  `PATH` varchar(200) NOT NULL,
  `DATE_CREATED` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `training_correlation`
--

CREATE TABLE `training_correlation` (
  `REQUEST_ID` int(11) NOT NULL,
  `WATT_HOURS` float NOT NULL,
  `PREDICTED_WATT_HOURS` float NOT NULL,
  `DATE` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `training_evaluation`
--

CREATE TABLE `training_evaluation` (
  `REQUEST_ID` int(11) NOT NULL,
  `ACCURACY` float NOT NULL,
  `LOSS` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `training_input`
--

CREATE TABLE `training_input` (
  `NODE_ID` int(11) NOT NULL,
  `SOURCE_ID` varchar(20) NOT NULL,
  `DATE_CREATED` datetime NOT NULL,
  `ENTRY_DATE` datetime NOT NULL,
  `PREV_WEEK_WATTHOURS` float NOT NULL,
  `PREV_2WEEK_WATTHOURS` float NOT NULL,
  `PRESSURE` float NOT NULL,
  `HUMIDITY` float NOT NULL,
  `TEMP` float NOT NULL,
  `CLOUDINESS` float NOT NULL,
  `WIND_SPEED` float NOT NULL,
  `WIND_DIR` float NOT NULL,
  `WATT_HOURS` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `training_parameters`
--

CREATE TABLE `training_parameters` (
  `REQUEST_ID` int(11) NOT NULL,
  `MAX_EPOCHS` int(11) NOT NULL,
  `BATCH_SIZE` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `training_requests`
--

CREATE TABLE `training_requests` (
  `REQUEST_ID` int(11) NOT NULL,
  `NAME` varchar(15) DEFAULT NULL,
  `NODE_ID` int(11) NOT NULL,
  `SOURCE_ID` varchar(20) NOT NULL,
  `DATE_REQUESTED` datetime NOT NULL,
  `STATUS` int(11) NOT NULL,
  `REQUEST_ENGINE` varchar(20) NOT NULL,
  `START_DATE` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `END_DATE` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `DYNAMIC` tinyint(1) NOT NULL DEFAULT '0',
  `NOTES` mediumtext NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `training_state_time`
--

CREATE TABLE `training_state_time` (
  `REQUEST_ID` int(11) NOT NULL,
  `STATE` int(11) NOT NULL,
  `START_DATE` datetime NOT NULL,
  `COMPLETION_DATE` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `weather_data`
--

CREATE TABLE `weather_data` (
  `DATE_CREATED` datetime NOT NULL,
  `SKY` varchar(20) NOT NULL,
  `TEMP` int(10) NOT NULL,
  `HUMIDITY` int(10) NOT NULL,
  `ATM` int(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `yr_weather`
--

CREATE TABLE `yr_weather` (
  `PREDICTION_DATE` datetime NOT NULL,
  `TEMP` float NOT NULL,
  `WIND_DIRECTION` float NOT NULL,
  `WIND_SPEED` float NOT NULL,
  `HUMIDITY` float NOT NULL,
  `PRESSURE` float NOT NULL,
  `CLOUDINESS` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `analysis_engine`
--
ALTER TABLE `analysis_engine`
  ADD PRIMARY KEY (`analysis_engine_code`),
  ADD KEY `consump1` (`analysis_engine_id`),
  ADD KEY `cd_main_index` (`analysis_engine_id`);

--
-- Indexes for table `node_datum`
--
ALTER TABLE `node_datum`
  ADD PRIMARY KEY (`NODE_ID`,`SOURCE_ID`,`DATE_CREATED`),
  ADD KEY `NODE_ID` (`NODE_ID`),
  ADD KEY `DATE_CREATED` (`DATE_CREATED`);

--
-- Indexes for table `node_source`
--
ALTER TABLE `node_source`
  ADD PRIMARY KEY (`node_id`,`sourceId`),
  ADD KEY `ns_main_index` (`node_id`,`sourceId`,`source_type_id`);

--
-- Indexes for table `owm_data`
--
ALTER TABLE `owm_data`
  ADD PRIMARY KEY (`DATE_CREATED`);

--
-- Indexes for table `prediction_input`
--
ALTER TABLE `prediction_input`
  ADD PRIMARY KEY (`NODE_ID`,`SOURCE_ID`,`DATE_PREDICTING`),
  ADD KEY `NODE_ID` (`NODE_ID`),
  ADD KEY `SOURCE_ID` (`SOURCE_ID`),
  ADD KEY `DATE_PREDICTING` (`DATE_PREDICTING`);

--
-- Indexes for table `prediction_output`
--
ALTER TABLE `prediction_output`
  ADD PRIMARY KEY (`REQUEST_ID`,`DATE`);

--
-- Indexes for table `prediction_requests`
--
ALTER TABLE `prediction_requests`
  ADD PRIMARY KEY (`REQUEST_ID`),
  ADD KEY `REQUEST_ID` (`REQUEST_ID`);

--
-- Indexes for table `registered_nodes`
--
ALTER TABLE `registered_nodes`
  ADD PRIMARY KEY (`NODE_ID`);

--
-- Indexes for table `requests`
--
ALTER TABLE `requests`
  ADD PRIMARY KEY (`REQUEST_ID`);

--
-- Indexes for table `training_correlation`
--
ALTER TABLE `training_correlation`
  ADD PRIMARY KEY (`REQUEST_ID`,`DATE`),
  ADD KEY `REQUEST_ID` (`REQUEST_ID`);

--
-- Indexes for table `training_evaluation`
--
ALTER TABLE `training_evaluation`
  ADD PRIMARY KEY (`REQUEST_ID`);

--
-- Indexes for table `training_input`
--
ALTER TABLE `training_input`
  ADD PRIMARY KEY (`NODE_ID`,`SOURCE_ID`,`DATE_CREATED`),
  ADD KEY `NODE_ID` (`NODE_ID`),
  ADD KEY `DATE_CREATED` (`DATE_CREATED`),
  ADD KEY `ENTRY_DATE` (`ENTRY_DATE`);

--
-- Indexes for table `training_requests`
--
ALTER TABLE `training_requests`
  ADD PRIMARY KEY (`REQUEST_ID`),
  ADD KEY `REQUEST_ID` (`REQUEST_ID`),
  ADD KEY `REQUEST_ID_2` (`REQUEST_ID`),
  ADD KEY `DATE_REQUESTED` (`DATE_REQUESTED`);

--
-- Indexes for table `training_state_time`
--
ALTER TABLE `training_state_time`
  ADD PRIMARY KEY (`REQUEST_ID`,`STATE`);

--
-- Indexes for table `weather_data`
--
ALTER TABLE `weather_data`
  ADD PRIMARY KEY (`DATE_CREATED`),
  ADD KEY `DATE_CREATED` (`DATE_CREATED`);

--
-- Indexes for table `yr_weather`
--
ALTER TABLE `yr_weather`
  ADD PRIMARY KEY (`PREDICTION_DATE`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `analysis_engine`
--
ALTER TABLE `analysis_engine`
  MODIFY `analysis_engine_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
--
-- AUTO_INCREMENT for table `prediction_requests`
--
ALTER TABLE `prediction_requests`
  MODIFY `REQUEST_ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=62;
--
-- AUTO_INCREMENT for table `requests`
--
ALTER TABLE `requests`
  MODIFY `REQUEST_ID` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `training_requests`
--
ALTER TABLE `training_requests`
  MODIFY `REQUEST_ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=207;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
