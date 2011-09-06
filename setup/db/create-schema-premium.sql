SET foreign_key_checks = 0;
DROP TABLE IF EXISTS `cloud_usage`.`event`;
DROP TABLE IF EXISTS `cloud_usage`.`cloud_usage`;
DROP TABLE IF EXISTS `cloud_usage`.`usage_vm_instance`;
DROP TABLE IF EXISTS `cloud_usage`.`usage_ip_address`;
DROP TABLE IF EXISTS `cloud_usage`.`usage_network`;
DROP TABLE IF EXISTS `cloud_usage`.`usage_job`;
DROP TABLE IF EXISTS `cloud_usage`.`account`;
DROP TABLE IF EXISTS `cloud_usage`.`user_statistics`;
DROP TABLE IF EXISTS `cloud_usage`.`usage_volume`;
DROP TABLE IF EXISTS `cloud_usage`.`usage_storage`;
DROP TABLE IF EXISTS `cloud_usage`.`usage_security_group`;
DROP TABLE IF EXISTS `cloud_usage`.`usage_load_balancer_policy`;
DROP TABLE IF EXISTS `cloud_usage`.`usage_port_forwarding`;
DROP TABLE IF EXISTS `cloud_usage`.`usage_network_offering`;
DROP TABLE IF EXISTS `cloud_usage`.`usage_event`;

CREATE TABLE  `cloud_usage`.`event` (
  `id` bigint unsigned NOT NULL auto_increment,
  `type` varchar(32) NOT NULL,
  `description` varchar(1024) NOT NULL,
  `user_id` bigint unsigned NOT NULL,
  `account_id` bigint unsigned NOT NULL,
  `created` datetime NOT NULL,
  `level` varchar(16) NOT NULL,
  `parameters` varchar(1024) NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE  `cloud_usage`.`cloud_usage` (
  `id` bigint unsigned NOT NULL auto_increment,
  `zone_id` bigint unsigned NOT NULL,
  `account_id` bigint unsigned NOT NULL,
  `domain_id` bigint unsigned NOT NULL,
  `description` varchar(1024) NOT NULL,
  `usage_display` varchar(255) NOT NULL,
  `usage_type` int(1) unsigned,
  `raw_usage` DOUBLE UNSIGNED NOT NULL,
  `vm_instance_id` bigint unsigned,
  `vm_name` varchar(255),
  `offering_id` bigint unsigned,
  `template_id` bigint unsigned,
  `usage_id` bigint unsigned,
  `type` varchar(32),
  `size` bigint unsigned,
  `network_id` bigint unsigned,
  `start_date` DATETIME NOT NULL,
  `end_date` DATETIME NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE  `cloud_usage`.`usage_vm_instance` (
  `usage_type` int(1) unsigned,
  `zone_id` bigint unsigned NOT NULL,
  `account_id` bigint unsigned NOT NULL,
  `vm_instance_id` bigint unsigned NOT NULL,
  `vm_name` varchar(255) NOT NULL,
  `service_offering_id` bigint unsigned NOT NULL,
  `template_id` bigint unsigned NOT NULL,
  `hypervisor_type` varchar(255),
  `start_date` DATETIME NOT NULL,
  `end_date` DATETIME NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE  `cloud_usage`.`usage_network` (
  `account_id` bigint unsigned NOT NULL,
  `zone_id` bigint unsigned NOT NULL,
  `host_id` bigint unsigned NOT NULL,
  `host_type` varchar(32),
  `network_id` bigint unsigned,
  `bytes_sent` bigint unsigned NOT NULL default '0',
  `bytes_received` bigint unsigned NOT NULL default '0',
  `net_bytes_received` bigint unsigned NOT NULL default '0',
  `net_bytes_sent` bigint unsigned NOT NULL default '0',
  `current_bytes_received` bigint unsigned NOT NULL default '0',
  `current_bytes_sent` bigint unsigned NOT NULL default '0',
  `event_time_millis` bigint unsigned NOT NULL default '0',
  PRIMARY KEY (`account_id`, `zone_id`, `host_id`, `event_time_millis`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE  `cloud_usage`.`usage_ip_address` (
  `id` bigint unsigned NOT NULL,
  `account_id` bigint unsigned NOT NULL,
  `domain_id` bigint unsigned NOT NULL,
  `zone_id` bigint unsigned NOT NULL,
  `public_ip_address` varchar(15) NOT NULL,
  `is_source_nat` smallint(1) NOT NULL,
  `assigned` DATETIME NOT NULL,
  `released` DATETIME NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE  `cloud_usage`.`usage_job` (
  `id` bigint unsigned NOT NULL auto_increment,
  `host` varchar(255),
  `pid` int(5),
  `job_type` int(1),
  `scheduled` int(1),
  `start_millis` bigint unsigned NOT NULL default '0' COMMENT 'start time in milliseconds of the aggregation range used by this job',
  `end_millis` bigint unsigned NOT NULL default '0' COMMENT 'end time in milliseconds of the aggregation range used by this job',
  `exec_time` bigint unsigned NOT NULL default '0' COMMENT 'how long in milliseconds it took for the job to execute',
  `start_date` DATETIME COMMENT 'start date of the aggregation range used by this job',
  `end_date` DATETIME COMMENT 'end date of the aggregation range used by this job',
  `success` int(1),
  `heartbeat` DATETIME NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE  `cloud_usage`.`account` (
  `id` bigint unsigned NOT NULL,
  `account_name` varchar(100) COMMENT 'an account name set by the creator of the account, defaults to username for single accounts',
  `type` int(1) unsigned NOT NULL,
  `domain_id` bigint unsigned,
  `state` varchar(10) NOT NULL default 'enabled',
  `removed` datetime COMMENT 'date removed',
  `cleanup_needed` tinyint(1) NOT NULL default '0',
  `network_domain` varchar(100) COMMENT 'Network domain name of the Vms of the account',
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE  `cloud_usage`.`user_statistics` (
  `id` bigint unsigned UNIQUE NOT NULL,
  `data_center_id` bigint unsigned NOT NULL,
  `account_id` bigint unsigned NOT NULL,
  `public_ip_address` varchar(15),
  `device_id` bigint unsigned NOT NULL,
  `device_type` varchar(32) NOT NULL,
  `network_id` bigint unsigned,
  `net_bytes_received` bigint unsigned NOT NULL default '0',
  `net_bytes_sent` bigint unsigned NOT NULL default '0',
  `current_bytes_received` bigint unsigned NOT NULL default '0',
  `current_bytes_sent` bigint unsigned NOT NULL default '0',
  PRIMARY KEY  (`id`),
  UNIQUE KEY (`account_id`, `data_center_id`, `public_ip_address`, `device_id`, `device_type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE  `cloud_usage`.`usage_volume` (
  `id` bigint unsigned NOT NULL,
  `zone_id` bigint unsigned NOT NULL,
  `account_id` bigint unsigned NOT NULL,
  `domain_id` bigint unsigned NOT NULL,
  `disk_offering_id` bigint unsigned,
  `template_id` bigint unsigned,
  `size` bigint unsigned,
  `created` DATETIME NOT NULL,
  `deleted` DATETIME NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE  `cloud_usage`.`usage_storage` (
  `id` bigint unsigned NOT NULL,
  `zone_id` bigint unsigned NOT NULL,
  `account_id` bigint unsigned NOT NULL,
  `domain_id` bigint unsigned NOT NULL,
  `storage_type` int(1) unsigned NOT NULL,
  `source_id` bigint unsigned,
  `size` bigint unsigned NOT NULL,
  `created` DATETIME NOT NULL,
  `deleted` DATETIME NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE  `cloud_usage`.`usage_security_group` (
  `id` bigint unsigned NOT NULL,
  `zone_id` bigint unsigned NOT NULL,
  `account_id` bigint unsigned NOT NULL,
  `domain_id` bigint unsigned NOT NULL,
  `vm_id` bigint unsigned NOT NULL,
  `num_rules` bigint unsigned NOT NULL,
  `created` DATETIME NOT NULL,
  `deleted` DATETIME NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE  `cloud_usage`.`usage_load_balancer_policy` (
  `id` bigint unsigned NOT NULL,
  `zone_id` bigint unsigned NOT NULL,
  `account_id` bigint unsigned NOT NULL,
  `domain_id` bigint unsigned NOT NULL,
  `created` DATETIME NOT NULL,
  `deleted` DATETIME NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE  `cloud_usage`.`usage_event` (
  `id` bigint unsigned NOT NULL auto_increment,
  `type` varchar(32) NOT NULL,
  `account_id` bigint unsigned NOT NULL,
  `created` datetime NOT NULL,
  `zone_id` bigint unsigned NOT NULL,
  `resource_id` bigint unsigned,
  `resource_name` varchar(255),
  `offering_id` bigint unsigned,
  `template_id` bigint unsigned,
  `size` bigint unsigned,
  `resource_type` varchar(32),  
  `processed` tinyint NOT NULL default '0',
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE  `cloud_usage`.`usage_port_forwarding` (
  `id` bigint unsigned NOT NULL,
  `zone_id` bigint unsigned NOT NULL,
  `account_id` bigint unsigned NOT NULL,
  `domain_id` bigint unsigned NOT NULL,
  `created` DATETIME NOT NULL,
  `deleted` DATETIME NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE  `cloud_usage`.`usage_network_offering` (
  `zone_id` bigint unsigned NOT NULL,
  `account_id` bigint unsigned NOT NULL,
  `domain_id` bigint unsigned NOT NULL,
  `vm_instance_id` bigint unsigned NOT NULL,
  `network_offering_id` bigint unsigned NOT NULL,
  `is_default` smallint(1) NOT NULL,
  `created` DATETIME NOT NULL,
  `deleted` DATETIME NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `cloud`.`netapp_volume` (
  `id` bigint unsigned NOT NULL UNIQUE AUTO_INCREMENT COMMENT 'id',
  `ip_address` varchar(255) NOT NULL COMMENT 'ip address/fqdn of the volume',
  `pool_id` bigint unsigned NOT NULL COMMENT 'id for the pool',
  `pool_name` varchar(255) NOT NULL COMMENT 'name for the pool',
  `aggregate_name` varchar(255) NOT NULL COMMENT 'name for the aggregate',
  `volume_name` varchar(255) NOT NULL COMMENT 'name for the volume',
  `volume_size` varchar(255) NOT NULL COMMENT 'volume size',
  `snapshot_policy` varchar(255) NOT NULL COMMENT 'snapshot policy',
  `snapshot_reservation` int NOT NULL COMMENT 'snapshot reservation',  
  `username` varchar(255) NOT NULL COMMENT 'username',  
  `password` varchar(200) COMMENT 'password',
  `round_robin_marker` int COMMENT 'This marks the volume to be picked up for lun creation, RR fashion',
  PRIMARY KEY  (`id`),
  CONSTRAINT `fk_netapp_volume__pool_id` FOREIGN KEY `fk_netapp_volume__pool_id` (`pool_id`) REFERENCES `netapp_pool` (`id`) ON DELETE CASCADE,
  INDEX `i_netapp_volume__pool_id`(`pool_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `cloud`.`netapp_pool` (
  `id` bigint unsigned NOT NULL UNIQUE AUTO_INCREMENT COMMENT 'id',
  `name` varchar(255) NOT NULL UNIQUE COMMENT 'name for the pool',
  `algorithm` varchar(255) NOT NULL COMMENT 'algorithm',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `cloud`.`netapp_lun` (
  `id` bigint unsigned NOT NULL UNIQUE AUTO_INCREMENT COMMENT 'id',
  `lun_name` varchar(255) NOT NULL COMMENT 'lun name',
  `target_iqn` varchar(255) NOT NULL COMMENT 'target iqn',
  `path` varchar(255) NOT NULL COMMENT 'lun path',
  `size` bigint NOT NULL COMMENT 'lun size',
  `volume_id` bigint unsigned NOT NULL COMMENT 'parent volume id',
  PRIMARY KEY (`id`),
  CONSTRAINT `fk_netapp_lun__volume_id` FOREIGN KEY `fk_netapp_lun__volume_id` (`volume_id`) REFERENCES `netapp_volume` (`id`) ON DELETE CASCADE,
  INDEX `i_netapp_lun__volume_id`(`volume_id`),
  INDEX `i_netapp_lun__lun_name`(`lun_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

SET foreign_key_checks = 1;