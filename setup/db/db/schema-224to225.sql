# Copyright (C) 2011 Citrix Systems, Inc.  All rights reserved
#     
# This software is licensed under the GNU General Public License v3 or later.
# 
# It is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# 
--;
-- Schema upgrade from 2.2.4 to 2.2.5;
--;

ALTER TABLE `cloud`.`security_group` add UNIQUE KEY (`name`, `account_id`);
ALTER TABLE `cloud`.`storage_pool` MODIFY `host_address` varchar(255) NOT NULL;

CREATE TABLE IF NOT EXISTS `cloud`.`ovs_tunnel`(
  `id` bigint unsigned NOT NULL UNIQUE AUTO_INCREMENT,
  `from` bigint unsigned COMMENT 'from host id',
  `to` bigint unsigned COMMENT 'to host id',
  `key` int unsigned default '0' COMMENT 'current gre key can be used',
  PRIMARY KEY(`from`, `to`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `cloud`.`ovs_tunnel_account`(
  `id` bigint unsigned NOT NULL UNIQUE AUTO_INCREMENT,
  `from` bigint unsigned COMMENT 'from host id',
  `to` bigint unsigned COMMENT 'to host id',
  `account` bigint unsigned COMMENT 'account',
  `key` int unsigned COMMENT 'gre key',
  `port_name` varchar(32) COMMENT 'in port on open vswitch',
  `state` varchar(16) default 'FAILED' COMMENT 'result of tunnel creatation',
  PRIMARY KEY(`from`, `to`, `account`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE IF NOT EXISTS `cloud`.`storage_pool_work` (
  `id` bigint unsigned UNIQUE NOT NULL AUTO_INCREMENT COMMENT 'id',
  `pool_id` bigint unsigned NOT NULL COMMENT 'storage pool associated with the vm',
  `vm_id` bigint unsigned NOT NULL COMMENT 'vm identifier',
  `stopped_for_maintenance` tinyint unsigned NOT NULL DEFAULT 0 COMMENT 'this flag denoted whether the vm was stopped during maintenance',
  `started_after_maintenance` tinyint unsigned NOT NULL DEFAULT 0 COMMENT 'this flag denoted whether the vm was started after maintenance',
  `mgmt_server_id` bigint unsigned NOT NULL COMMENT 'management server id',
  PRIMARY KEY (`id`),
 UNIQUE (pool_id,vm_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


ALTER TABLE `cloud`.`firewall_rules` MODIFY `start_port` int(10) NOT NULL COMMENT 'starting port of a port range';
ALTER TABLE `cloud`.`firewall_rules` MODIFY `end_port` int(10) NOT NULL COMMENT 'end port of a port range';

ALTER TABLE `cloud`.`vm_template` MODIFY `extractable` int(1) unsigned NOT NULL default 0 COMMENT 'Is this template extractable';


ALTER TABLE `cloud`.`user_statistics` MODIFY `device_id` bigint(20) unsigned NOT NULL;
ALTER TABLE `cloud`.`user_statistics` MODIFY `device_type` varchar(32) NOT NULL;

ALTER TABLE `cloud`.`nics` MODIFY `ip6_address` char(40);

