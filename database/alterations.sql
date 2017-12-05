#2014.12.30

ALTER TABLE  `training_file` ADD  `input_weights_file_name` VARCHAR( 255 ) NOT NULL AFTER  `created_on` ;
ALTER TABLE  `training_file` ADD  `output_weights_file_name` VARCHAR( 255 ) NOT NULL AFTER  `input_weights_file_name` ;
ALTER TABLE  `training_file` ADD  `input_file_name` VARCHAR( 255 ) NOT NULL AFTER  `output_weights_file_name` ;
ALTER TABLE  `training_file` ADD  `output_file_name` VARCHAR( 255 ) NOT NULL AFTER  `input_file_name` ;
ALTER TABLE  `training_file` ADD  `emergent_log_file_name` VARCHAR( 255 ) NOT NULL AFTER  `output_file_name` ;

#2015.01.29
ALTER TABLE `node` CHANGE `source_ids` `subscribed_source_ids` VARCHAR(255) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL;

#2015.01.30
ALTER TABLE `patternset_node_match` DROP INDEX `pnm_main_index`;
ALTER TABLE `patternset_node_match` ADD INDEX `pnm_main_index` (`pattern_set_id`, `node_id`);

ALTER TABLE `node` DROP INDEX `n_main_index`;
ALTER TABLE `node` ADD INDEX `n_main_index` (`node_id`, `node_type_id`, `location`, `is_subscribed_for_training`);

ALTER TABLE `power_datum` DROP INDEX `pd_main_index`;
ALTER TABLE `power_datum` ADD INDEX `pd_main_index` (`power_datum_id`, `when_logged`);

ALTER TABLE `consumption_datum` DROP INDEX `cd_main_index`;
ALTER TABLE `consumption_datum` ADD INDEX `cd_main_index` (`consumption_datum_id`, `when_logged`, `amps`);

ALTER TABLE `node_source` DROP INDEX `ns_main_index`;
ALTER TABLE `node_source` ADD INDEX `ns_main_index` (`node_id`, `sourceId`,`source_type_id`);

ALTER TABLE `training_file` DROP INDEX `tf_main_index`;
ALTER TABLE `training_file` ADD INDEX `tf_main_index` (`pattern_set_id`, `created_on`,`status_id`,`start_training`, `stop_training`);

ALTER TABLE `training_datum` DROP INDEX `td_main_index`;
ALTER TABLE `training_datum` ADD INDEX `td_main_index` (`training_datum_id`, `training_file_id`,`when_logged`);

ALTER TABLE `solar_error` DROP INDEX `se_main_index`;
ALTER TABLE `solar_error` ADD INDEX `se_main_index` (`solar_error_id`, `when_logged`);

ALTER TABLE `consumption_input_pattern` DROP INDEX `cip_main_index`;
ALTER TABLE `consumption_input_pattern` ADD INDEX `cip_main_index` (`consumption_input_pattern_id`,`node_id`,`pattern_set_id`, `trial_name`, `start_datetime`, `end_datetime`);
ALTER TABLE `consumption_input_pattern` DROP INDEX `cip_trialname_index`;
ALTER TABLE `consumption_input_pattern` ADD INDEX `cip_trialname_index` (`consumption_input_pattern_id`,`trial_name`);

#2015.02.19
ALTER TABLE  `consumption_input_pattern` ADD  `predicted_kilowatt_hours_weight` float NOT NULL AFTER  `kilowatt_hours_weight` ;

#2015.02.24
ALTER TABLE  `consumption_input_pattern` ADD  `trial_name` VARCHAR( 255 ) NOT NULL AFTER  `consumption_input_pattern_id` ;

#2016.03.19
ALTER TABLE `inputpattern_extensions` DROP INDEX `ie_main_index`;
ALTER TABLE `inputpattern_extensions` ADD INDEX `ie_main_index` (`extension_id`,`consumption_input_pattern_id`);

INSERT INTO inputpattern_extensions (consumption_input_pattern_id, predicted_kilowatt_hours_weight) SELECT consumption_input_pattern_id, predicted_kilowatt_hours_weight FROM consumption_input_pattern;

#2016.07.06
ALTER TABLE  `weather_datum` ADD  `status_id` int(11) NULL AFTER  `weather_datum_id` ;

#2017.09.23
ALTER TABLE `solar_error` DROP INDEX `se_module_index`;
ALTER TABLE `solar_error` ADD INDEX `se_module_index` (`module`);

