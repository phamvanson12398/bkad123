/*
 Navicat Premium Data Transfer

 Source Server         : abc
 Source Server Type    : MySQL
 Source Server Version : 50730
 Source Host           : 192.168.200.4:3306
 Source Schema         : bkad

 Target Server Type    : MySQL
 Target Server Version : 50730
 File Encoding         : 65001

 Date: 14/07/2020 09:55:18
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for abnormal
-- ----------------------------
DROP TABLE IF EXISTS `abnormal`;
CREATE TABLE `abnormal`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `description` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `status` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `ad_profile` int(11) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `fk_profile_2`(`ad_profile`) USING BTREE,
  CONSTRAINT `fk_profile_2` FOREIGN KEY (`ad_profile`) REFERENCES `ad_profile` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of abnormal
-- ----------------------------

-- ----------------------------
-- Table structure for access_control_list
-- ----------------------------
DROP TABLE IF EXISTS `access_control_list`;
CREATE TABLE `access_control_list`  (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `address` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `type` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `description` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `status` int(255) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 5 CHARACTER SET = utf8 COLLATE = utf8_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of access_control_list
-- ----------------------------
INSERT INTO `access_control_list` VALUES (3, '10.2.32.113', 'blacklist', 'test 1', 1);
INSERT INTO `access_control_list` VALUES (4, '10.2.32.113', 'blacklist', 'test 2', 1);

-- ----------------------------
-- Table structure for acsh
-- ----------------------------
DROP TABLE IF EXISTS `acsh`;
CREATE TABLE `acsh`  (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `address` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `domain` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `service_status` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `status` int(10) NULL DEFAULT NULL,
  `port` int(10) NULL DEFAULT NULL,
  `description` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8 COLLATE = utf8_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of acsh
-- ----------------------------
INSERT INTO `acsh` VALUES (2, '10.2.32.113', 'bkav.com', 'offline', 1, 80, 'test put');
INSERT INTO `acsh` VALUES (3, '10.2.32.113', 'bkav.com', 'online', 1, 80, 'test');

-- ----------------------------
-- Table structure for ad_policy
-- ----------------------------
DROP TABLE IF EXISTS `ad_policy`;
CREATE TABLE `ad_policy`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `profile` int(11) NULL DEFAULT NULL,
  `description` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `status` int(11) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `fk_profile`(`profile`) USING BTREE,
  CONSTRAINT `fk_profile` FOREIGN KEY (`profile`) REFERENCES `ad_profile` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8 COLLATE = utf8_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of ad_policy
-- ----------------------------
INSERT INTO `ad_policy` VALUES (1, 'Policy 1', 2, 'test', 1);

-- ----------------------------
-- Table structure for ad_policy_have_group_networks
-- ----------------------------
DROP TABLE IF EXISTS `ad_policy_have_group_networks`;
CREATE TABLE `ad_policy_have_group_networks`  (
  `policy_id` int(11) NOT NULL,
  `group_network_id` int(11) NOT NULL,
  PRIMARY KEY (`policy_id`, `group_network_id`) USING BTREE,
  INDEX `fk_group_network1`(`group_network_id`) USING BTREE,
  CONSTRAINT `fk_group_network1` FOREIGN KEY (`group_network_id`) REFERENCES `group_network` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_policy1` FOREIGN KEY (`policy_id`) REFERENCES `ad_policy` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of ad_policy_have_group_networks
-- ----------------------------
INSERT INTO `ad_policy_have_group_networks` VALUES (1, 1);

-- ----------------------------
-- Table structure for ad_policy_have_networks
-- ----------------------------
DROP TABLE IF EXISTS `ad_policy_have_networks`;
CREATE TABLE `ad_policy_have_networks`  (
  `policy_id` int(11) NOT NULL,
  `network_id` int(11) NOT NULL,
  PRIMARY KEY (`policy_id`, `network_id`) USING BTREE,
  INDEX `fk_network`(`network_id`) USING BTREE,
  CONSTRAINT `fk_network` FOREIGN KEY (`network_id`) REFERENCES `network` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_policy` FOREIGN KEY (`policy_id`) REFERENCES `ad_policy` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of ad_policy_have_networks
-- ----------------------------
INSERT INTO `ad_policy_have_networks` VALUES (1, 2);

-- ----------------------------
-- Table structure for ad_profile
-- ----------------------------
DROP TABLE IF EXISTS `ad_profile`;
CREATE TABLE `ad_profile`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `mode` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `description` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 17 CHARACTER SET = utf8 COLLATE = utf8_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of ad_profile
-- ----------------------------
INSERT INTO `ad_profile` VALUES (1, 'Policy 1', 'detection', 'test');
INSERT INTO `ad_profile` VALUES (2, 'test 2', 'detection', 'abc');
INSERT INTO `ad_profile` VALUES (3, 'Profile 1', 'detection', 'test');
INSERT INTO `ad_profile` VALUES (4, 'Profile 2', 'detection', 'test');
INSERT INTO `ad_profile` VALUES (5, 'Profile 2', 'detection', 'test');
INSERT INTO `ad_profile` VALUES (6, 'Profile 2', 'detection', 'test');
INSERT INTO `ad_profile` VALUES (7, 'Profile 2', 'detection', 'test');
INSERT INTO `ad_profile` VALUES (10, 'test', 'prevention', 'abc');
INSERT INTO `ad_profile` VALUES (11, 'test add data', 'prevention', 'abc');
INSERT INTO `ad_profile` VALUES (12, 'test add data', 'prevention', 'abc');
INSERT INTO `ad_profile` VALUES (13, 'test add data', 'prevention', 'abc');
INSERT INTO `ad_profile` VALUES (14, 'test add data', 'prevention', 'abc');
INSERT INTO `ad_profile` VALUES (15, 'test add data', 'prevention', 'abc');
INSERT INTO `ad_profile` VALUES (16, 'test add data', 'prevention', 'abc');

-- ----------------------------
-- Table structure for atas
-- ----------------------------
DROP TABLE IF EXISTS `atas`;
CREATE TABLE `atas`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `learning_mode` int(11) NULL DEFAULT NULL,
  `start_time` datetime(0) NULL DEFAULT NULL,
  `start_date` datetime(0) NULL DEFAULT NULL,
  `end_date` datetime(0) NULL DEFAULT NULL,
  `apply` int(11) NULL DEFAULT NULL,
  `status` int(11) NULL DEFAULT 1,
  `progress` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT '0',
  `profile` int(11) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `fl_ad_profile`(`name`) USING BTREE,
  INDEX `fk_learning_mode`(`learning_mode`) USING BTREE,
  INDEX `fk_profile3`(`profile`) USING BTREE,
  CONSTRAINT `fk_learning_mode` FOREIGN KEY (`learning_mode`) REFERENCES `learning_mode` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_profile3` FOREIGN KEY (`profile`) REFERENCES `ad_profile` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB AUTO_INCREMENT = 13 CHARACTER SET = utf8 COLLATE = utf8_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of atas
-- ----------------------------
INSERT INTO `atas` VALUES (2, '1', 1, '2020-05-01 13:27:00', '2020-05-07 13:27:05', '2020-05-14 13:27:09', 1, 1, '0', 3);
INSERT INTO `atas` VALUES (3, 'Profile 2', 0, '2020-05-29 13:56:04', '2020-05-29 13:56:04', '2020-05-29 13:56:04', 1, 0, 'Not yet started', 7);
INSERT INTO `atas` VALUES (6, 'test', 0, '2020-06-04 10:31:10', '2020-06-04 10:31:10', '2020-06-04 10:31:10', 1, 0, 'Not yet started', 10);
INSERT INTO `atas` VALUES (7, 'test add data', 0, '2020-06-04 10:37:32', '2020-06-04 10:37:32', '2020-06-04 10:37:32', 1, 0, 'Not yet started', 11);
INSERT INTO `atas` VALUES (8, 'test add data', 0, '2020-06-04 10:38:18', '2020-06-04 10:38:18', '2020-06-04 10:38:18', 1, 0, 'Not yet started', 12);
INSERT INTO `atas` VALUES (9, 'test add data', 0, '2020-06-04 10:46:13', '2020-06-04 10:46:13', '2020-06-04 10:46:13', 1, 0, 'Not yet started', 13);
INSERT INTO `atas` VALUES (10, 'test add data', 0, '2020-06-04 10:48:40', '2020-06-04 10:48:40', '2020-06-04 10:48:40', 1, 0, 'Not yet started', 14);
INSERT INTO `atas` VALUES (11, 'test add data', 0, '2020-06-04 11:17:26', '2020-06-04 11:17:26', '2020-06-04 11:17:26', 1, 0, 'Not yet started', 15);
INSERT INTO `atas` VALUES (12, 'test add data', 0, '2020-06-04 11:27:09', '2020-06-04 11:27:09', '2020-06-04 11:27:09', 1, 0, 'Not yet started', 16);

-- ----------------------------
-- Table structure for atas_http_threshold
-- ----------------------------
DROP TABLE IF EXISTS `atas_http_threshold`;
CREATE TABLE `atas_http_threshold`  (
  `id` int(11) NOT NULL,
  `threshold_id` int(11) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `fk_threshold_id1`(`threshold_id`) USING BTREE,
  CONSTRAINT `fk_threshold_id1` FOREIGN KEY (`threshold_id`) REFERENCES `http_threshold` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of atas_http_threshold
-- ----------------------------

-- ----------------------------
-- Table structure for atas_tcp_threshold
-- ----------------------------
DROP TABLE IF EXISTS `atas_tcp_threshold`;
CREATE TABLE `atas_tcp_threshold`  (
  `id` int(11) NOT NULL,
  `tcp_threshold_id` int(11) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `fk_tcp_theshold_id`(`tcp_threshold_id`) USING BTREE,
  CONSTRAINT `fk_tcp_theshold_id` FOREIGN KEY (`tcp_threshold_id`) REFERENCES `tcp_threshold` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of atas_tcp_threshold
-- ----------------------------

-- ----------------------------
-- Table structure for backup
-- ----------------------------
DROP TABLE IF EXISTS `backup`;
CREATE TABLE `backup`  (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `description` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `datetime` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `password` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 5 CHARACTER SET = utf8 COLLATE = utf8_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of backup
-- ----------------------------
INSERT INTO `backup` VALUES (1, 'backup 1', 'abc', '2020-05-29 16:28:50.979127', '123456');
INSERT INTO `backup` VALUES (2, 'backup 2', 'abc', '2020-06-01 09:18:23.230290', '123456');
INSERT INTO `backup` VALUES (3, 'backup test', 'abc', '2020-06-01 10:04:59.110967', '123456');
INSERT INTO `backup` VALUES (4, 'backup sdjkbhfsjkdbkjs', 'abc', '2020-07-07 09:41:30.032831', '123456');

-- ----------------------------
-- Table structure for backup_plan
-- ----------------------------
DROP TABLE IF EXISTS `backup_plan`;
CREATE TABLE `backup_plan`  (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `status` int(10) NULL DEFAULT NULL,
  `frequency` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `specific_day` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `start_time` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `end_date` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `start_date` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 6 CHARACTER SET = utf8 COLLATE = utf8_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of backup_plan
-- ----------------------------
INSERT INTO `backup_plan` VALUES (5, 1, 'dayly', '22', '9:09 AM', '8/7/2020', '7/7/2020');

-- ----------------------------
-- Table structure for config_ha
-- ----------------------------
DROP TABLE IF EXISTS `config_ha`;
CREATE TABLE `config_ha`  (
  `id` int(10) NOT NULL,
  `device_priority` int(10) NULL DEFAULT NULL,
  `group_name` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `group_password` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `heartbeat_interfaces` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `heartbeat_netmask` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `heartbeat_network` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `operation_mode` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `high_availability_status` int(255) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of config_ha
-- ----------------------------
INSERT INTO `config_ha` VALUES (1, 230, 'Group-Bkav a put', '123456', 'port1', '255.255.255.0', '10.10.10.0', 'active-active', 1);

-- ----------------------------
-- Table structure for dashboard
-- ----------------------------
DROP TABLE IF EXISTS `dashboard`;
CREATE TABLE `dashboard`  (
  `id` int(11) NOT NULL,
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `version` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of dashboard
-- ----------------------------
INSERT INTO `dashboard` VALUES (1, 'BKAD 2020', '1.0.0 (Last update 01 - 01 - 2020)');

-- ----------------------------
-- Table structure for datetime
-- ----------------------------
DROP TABLE IF EXISTS `datetime`;
CREATE TABLE `datetime`  (
  `id` int(10) NOT NULL,
  `sync_time` int(10) NOT NULL,
  `system_time` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `time_zone` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `server` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of datetime
-- ----------------------------
INSERT INTO `datetime` VALUES (1, 1, '', '', 'abcd');

-- ----------------------------
-- Table structure for emegency
-- ----------------------------
DROP TABLE IF EXISTS `emegency`;
CREATE TABLE `emegency`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `number_of_event` int(10) NULL DEFAULT NULL,
  `time_limited` int(10) NULL DEFAULT NULL,
  `report_email` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8 COLLATE = utf8_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of emegency
-- ----------------------------
INSERT INTO `emegency` VALUES (2, 'test', 12, 12, 'A@gmail.com, B@gmail.com, C@gmail.com');

-- ----------------------------
-- Table structure for firewall_access
-- ----------------------------
DROP TABLE IF EXISTS `firewall_access`;
CREATE TABLE `firewall_access`  (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `position` int(10) NULL DEFAULT NULL,
  `action` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `status` int(10) NULL DEFAULT NULL,
  `created_at` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `edited_at` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `interface` int(10) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `interface_fk`(`interface`) USING BTREE,
  CONSTRAINT `interface_fk` FOREIGN KEY (`interface`) REFERENCES `network_interface` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB AUTO_INCREMENT = 12 CHARACTER SET = utf8 COLLATE = utf8_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of firewall_access
-- ----------------------------
INSERT INTO `firewall_access` VALUES (11, 'test2', 1, 'accept', 1, '2020-06-09 11:33:37.056882', '2020-06-09 11:33:37.056891', 12);

-- ----------------------------
-- Table structure for firewall_access_destination
-- ----------------------------
DROP TABLE IF EXISTS `firewall_access_destination`;
CREATE TABLE `firewall_access_destination`  (
  `firewall_id` int(10) NOT NULL,
  `network_id` int(10) NOT NULL,
  PRIMARY KEY (`firewall_id`, `network_id`) USING BTREE,
  INDEX `network1`(`network_id`) USING BTREE,
  CONSTRAINT `firewall2` FOREIGN KEY (`firewall_id`) REFERENCES `firewall_access` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `network1` FOREIGN KEY (`network_id`) REFERENCES `network` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of firewall_access_destination
-- ----------------------------
INSERT INTO `firewall_access_destination` VALUES (11, 2);

-- ----------------------------
-- Table structure for firewall_access_group_destination
-- ----------------------------
DROP TABLE IF EXISTS `firewall_access_group_destination`;
CREATE TABLE `firewall_access_group_destination`  (
  `firewall_id` int(10) NOT NULL,
  `gr_network_id` int(10) NOT NULL,
  PRIMARY KEY (`firewall_id`, `gr_network_id`) USING BTREE,
  INDEX `gr_network2`(`gr_network_id`) USING BTREE,
  CONSTRAINT `firewall3` FOREIGN KEY (`firewall_id`) REFERENCES `firewall_access` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `gr_network2` FOREIGN KEY (`gr_network_id`) REFERENCES `group_network` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of firewall_access_group_destination
-- ----------------------------
INSERT INTO `firewall_access_group_destination` VALUES (11, 1);

-- ----------------------------
-- Table structure for firewall_access_group_service
-- ----------------------------
DROP TABLE IF EXISTS `firewall_access_group_service`;
CREATE TABLE `firewall_access_group_service`  (
  `firewall_id` int(10) NOT NULL,
  `gr_service_id` int(10) NOT NULL,
  PRIMARY KEY (`firewall_id`, `gr_service_id`) USING BTREE,
  INDEX `gr_service`(`gr_service_id`) USING BTREE,
  CONSTRAINT `firewall5` FOREIGN KEY (`firewall_id`) REFERENCES `firewall_access` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `gr_service` FOREIGN KEY (`gr_service_id`) REFERENCES `group_service` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of firewall_access_group_service
-- ----------------------------
INSERT INTO `firewall_access_group_service` VALUES (11, 3);

-- ----------------------------
-- Table structure for firewall_access_group_source
-- ----------------------------
DROP TABLE IF EXISTS `firewall_access_group_source`;
CREATE TABLE `firewall_access_group_source`  (
  `firewall_id` int(10) NOT NULL,
  `gr_network_id` int(10) NOT NULL,
  PRIMARY KEY (`firewall_id`, `gr_network_id`) USING BTREE,
  INDEX `gr_network`(`gr_network_id`) USING BTREE,
  CONSTRAINT `firewall1` FOREIGN KEY (`firewall_id`) REFERENCES `firewall_access` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `gr_network` FOREIGN KEY (`gr_network_id`) REFERENCES `group_network` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of firewall_access_group_source
-- ----------------------------
INSERT INTO `firewall_access_group_source` VALUES (11, 1);

-- ----------------------------
-- Table structure for firewall_access_service
-- ----------------------------
DROP TABLE IF EXISTS `firewall_access_service`;
CREATE TABLE `firewall_access_service`  (
  `firewall_id` int(10) NOT NULL,
  `service_id` int(10) NOT NULL,
  PRIMARY KEY (`firewall_id`, `service_id`) USING BTREE,
  INDEX `service`(`service_id`) USING BTREE,
  CONSTRAINT `firewall4` FOREIGN KEY (`firewall_id`) REFERENCES `firewall_access` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `service` FOREIGN KEY (`service_id`) REFERENCES `service` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of firewall_access_service
-- ----------------------------
INSERT INTO `firewall_access_service` VALUES (11, 1);

-- ----------------------------
-- Table structure for firewall_access_source
-- ----------------------------
DROP TABLE IF EXISTS `firewall_access_source`;
CREATE TABLE `firewall_access_source`  (
  `firewall_id` int(10) NOT NULL,
  `network_id` int(10) NOT NULL,
  PRIMARY KEY (`firewall_id`, `network_id`) USING BTREE,
  INDEX `network`(`network_id`) USING BTREE,
  CONSTRAINT `firewall` FOREIGN KEY (`firewall_id`) REFERENCES `firewall_access` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `network` FOREIGN KEY (`network_id`) REFERENCES `network` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of firewall_access_source
-- ----------------------------
INSERT INTO `firewall_access_source` VALUES (11, 2);

-- ----------------------------
-- Table structure for group_nat_have_interface
-- ----------------------------
DROP TABLE IF EXISTS `group_nat_have_interface`;
CREATE TABLE `group_nat_have_interface`  (
  `interface_id` int(10) NOT NULL,
  `nat_id` int(10) NOT NULL,
  PRIMARY KEY (`interface_id`, `nat_id`) USING BTREE,
  INDEX `nat_id1`(`nat_id`) USING BTREE,
  CONSTRAINT `interface_id12` FOREIGN KEY (`interface_id`) REFERENCES `network_interface` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `nat_id1` FOREIGN KEY (`nat_id`) REFERENCES `network_nat` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of group_nat_have_interface
-- ----------------------------
INSERT INTO `group_nat_have_interface` VALUES (12, 11);
INSERT INTO `group_nat_have_interface` VALUES (14, 11);

-- ----------------------------
-- Table structure for group_network
-- ----------------------------
DROP TABLE IF EXISTS `group_network`;
CREATE TABLE `group_network`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `description` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8 COLLATE = utf8_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of group_network
-- ----------------------------
INSERT INTO `group_network` VALUES (1, 'Group11', '');

-- ----------------------------
-- Table structure for group_network_have_network
-- ----------------------------
DROP TABLE IF EXISTS `group_network_have_network`;
CREATE TABLE `group_network_have_network`  (
  `network_id` int(11) NOT NULL,
  `group_network_id` int(11) NOT NULL,
  PRIMARY KEY (`network_id`, `group_network_id`) USING BTREE,
  INDEX `fk_group_network_2`(`group_network_id`) USING BTREE,
  CONSTRAINT `fk_group_network_2` FOREIGN KEY (`group_network_id`) REFERENCES `group_network` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_network_2` FOREIGN KEY (`network_id`) REFERENCES `network` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of group_network_have_network
-- ----------------------------
INSERT INTO `group_network_have_network` VALUES (2, 1);

-- ----------------------------
-- Table structure for group_service
-- ----------------------------
DROP TABLE IF EXISTS `group_service`;
CREATE TABLE `group_service`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `description` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 9 CHARACTER SET = utf8 COLLATE = utf8_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of group_service
-- ----------------------------
INSERT INTO `group_service` VALUES (3, 'lab1', '');
INSERT INTO `group_service` VALUES (6, 'lab1', '');
INSERT INTO `group_service` VALUES (8, 'lab1', '');

-- ----------------------------
-- Table structure for group_service_have_services
-- ----------------------------
DROP TABLE IF EXISTS `group_service_have_services`;
CREATE TABLE `group_service_have_services`  (
  `service_id` int(11) NOT NULL,
  `group_service_id` int(11) NOT NULL,
  PRIMARY KEY (`group_service_id`, `service_id`) USING BTREE,
  INDEX `group_service_have_service_service_id_fk`(`service_id`) USING BTREE,
  CONSTRAINT `group_service_have_service_group_service_id_fk` FOREIGN KEY (`group_service_id`) REFERENCES `group_service` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `group_service_have_service_service_id_fk` FOREIGN KEY (`service_id`) REFERENCES `service` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of group_service_have_services
-- ----------------------------
INSERT INTO `group_service_have_services` VALUES (1, 6);
INSERT INTO `group_service_have_services` VALUES (1, 8);
INSERT INTO `group_service_have_services` VALUES (2, 6);
INSERT INTO `group_service_have_services` VALUES (2, 8);

-- ----------------------------
-- Table structure for group_websites
-- ----------------------------
DROP TABLE IF EXISTS `group_websites`;
CREATE TABLE `group_websites`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `description` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8 COLLATE = utf8_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of group_websites
-- ----------------------------
INSERT INTO `group_websites` VALUES (2, 'vvvvv', '');
INSERT INTO `group_websites` VALUES (3, 'vvvvv', '');

-- ----------------------------
-- Table structure for group_websites_have_websites
-- ----------------------------
DROP TABLE IF EXISTS `group_websites_have_websites`;
CREATE TABLE `group_websites_have_websites`  (
  `website_id` int(11) NOT NULL,
  `group_website_id` int(11) NOT NULL,
  PRIMARY KEY (`website_id`, `group_website_id`) USING BTREE,
  INDEX `fk_group_website`(`group_website_id`) USING BTREE,
  CONSTRAINT `fk_group_website` FOREIGN KEY (`group_website_id`) REFERENCES `group_websites` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_website` FOREIGN KEY (`website_id`) REFERENCES `websites` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of group_websites_have_websites
-- ----------------------------
INSERT INTO `group_websites_have_websites` VALUES (5, 2);
INSERT INTO `group_websites_have_websites` VALUES (6, 2);
INSERT INTO `group_websites_have_websites` VALUES (8, 2);
INSERT INTO `group_websites_have_websites` VALUES (5, 3);
INSERT INTO `group_websites_have_websites` VALUES (6, 3);
INSERT INTO `group_websites_have_websites` VALUES (8, 3);

-- ----------------------------
-- Table structure for http_threshold
-- ----------------------------
DROP TABLE IF EXISTS `http_threshold`;
CREATE TABLE `http_threshold`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `packet_in` int(11) NULL DEFAULT NULL,
  `packet_out` int(11) NULL DEFAULT NULL,
  `bandwidth_in` int(11) NULL DEFAULT NULL,
  `bandwidth_out` int(11) NULL DEFAULT NULL,
  `percent` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `description` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `prevention` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `status` int(11) NULL DEFAULT NULL,
  `type` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `profile` int(11) NULL DEFAULT NULL,
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `tcp_threshold_ad_profile_id_fk`(`profile`) USING BTREE,
  CONSTRAINT `http_threshold_ibfk_1` FOREIGN KEY (`profile`) REFERENCES `ad_profile` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB AUTO_INCREMENT = 9 CHARACTER SET = utf8 COLLATE = utf8_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of http_threshold
-- ----------------------------
INSERT INTO `http_threshold` VALUES (3, 100, 100, 100, 100, '20.7', 'abc', 'drop', 1, 'protocol', 2, 'test add');
INSERT INTO `http_threshold` VALUES (4, 100, 100, 100, 100, '20.7', 'abc', 'drop', 1, 'protocol', 2, 'test edit 123');
INSERT INTO `http_threshold` VALUES (7, 100, 100, 100, 100, '12.3', '', 'drop', 1, 'syn', 3, 'test add');
INSERT INTO `http_threshold` VALUES (8, 100, 100, 100, 100, '12.3', '', 'drop', 1, 'url', 3, 'test add');

-- ----------------------------
-- Table structure for http_threshold_value
-- ----------------------------
DROP TABLE IF EXISTS `http_threshold_value`;
CREATE TABLE `http_threshold_value`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `http_threshold_id` int(11) NULL DEFAULT NULL,
  `value` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `fk_http_threshold1`(`http_threshold_id`) USING BTREE,
  CONSTRAINT `fk_http_threshold1` FOREIGN KEY (`http_threshold_id`) REFERENCES `http_threshold` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB AUTO_INCREMENT = 16 CHARACTER SET = utf8 COLLATE = utf8_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of http_threshold_value
-- ----------------------------
INSERT INTO `http_threshold_value` VALUES (10, 7, 'test data 1');
INSERT INTO `http_threshold_value` VALUES (11, 7, 'test data 2');
INSERT INTO `http_threshold_value` VALUES (12, 7, 'test data 3');
INSERT INTO `http_threshold_value` VALUES (13, 8, 'test data 1');
INSERT INTO `http_threshold_value` VALUES (14, 8, 'test data 2');
INSERT INTO `http_threshold_value` VALUES (15, 8, 'test data 3');

-- ----------------------------
-- Table structure for learning_mode
-- ----------------------------
DROP TABLE IF EXISTS `learning_mode`;
CREATE TABLE `learning_mode`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `learning_time` int(11) NULL DEFAULT NULL,
  `iteration` int(11) NULL DEFAULT NULL,
  `learning_type` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8 COLLATE = utf8_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of learning_mode
-- ----------------------------
INSERT INTO `learning_mode` VALUES (0, 'Default', 1, 4, 'weeks');
INSERT INTO `learning_mode` VALUES (1, 'mode 1', 3, 3, 'weeks');
INSERT INTO `learning_mode` VALUES (2, 'test', 3, 3, 'days');

-- ----------------------------
-- Table structure for license
-- ----------------------------
DROP TABLE IF EXISTS `license`;
CREATE TABLE `license`  (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `email` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `key` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `expires` date NULL DEFAULT NULL,
  `status` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `name`(`name`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8 COLLATE = utf8_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of license
-- ----------------------------
INSERT INTO `license` VALUES (1, 'khanhkd', 'khanhkd@bkav.com', '1234567789', '2022-06-12', 'Active');

-- ----------------------------
-- Table structure for monitoring_system_resource
-- ----------------------------
DROP TABLE IF EXISTS `monitoring_system_resource`;
CREATE TABLE `monitoring_system_resource`  (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `ram` decimal(10, 0) NULL DEFAULT NULL,
  `cpu` decimal(10, 0) NULL DEFAULT NULL,
  `disk` int(10) NULL DEFAULT NULL,
  `created_at` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8 COLLATE = utf8_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of monitoring_system_resource
-- ----------------------------
INSERT INTO `monitoring_system_resource` VALUES (1, 50, 24, 12, '2020-06-09 14:21:19.179245');

-- ----------------------------
-- Table structure for monitoring_traffic_resource
-- ----------------------------
DROP TABLE IF EXISTS `monitoring_traffic_resource`;
CREATE TABLE `monitoring_traffic_resource`  (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `interface` int(10) NULL DEFAULT NULL,
  `bw_input` int(10) NULL DEFAULT NULL,
  `bw_output` int(10) NULL DEFAULT NULL,
  `created_at` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `interface_id`(`interface`) USING BTREE,
  CONSTRAINT `interface_id` FOREIGN KEY (`interface`) REFERENCES `network_interface` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of monitoring_traffic_resource
-- ----------------------------

-- ----------------------------
-- Table structure for network
-- ----------------------------
DROP TABLE IF EXISTS `network`;
CREATE TABLE `network`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `ip_address` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `netmask` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `description` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8 COLLATE = utf8_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of network
-- ----------------------------
INSERT INTO `network` VALUES (2, 'Network1', '10.2.32.0', '255.255.255.0', 'test edit');

-- ----------------------------
-- Table structure for network_interface
-- ----------------------------
DROP TABLE IF EXISTS `network_interface`;
CREATE TABLE `network_interface`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `ip_address` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `netmask` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `gateway` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `status` int(11) NULL DEFAULT NULL,
  `type` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `addressing_mode` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `ispname` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `username` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `password` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `mtu` int(11) NULL DEFAULT NULL,
  `fixed_ip` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `clone_mac` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `updated_at` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `created_at` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `unique_name`(`name`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 36 CHARACTER SET = utf8 COLLATE = utf8_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of network_interface
-- ----------------------------
INSERT INTO `network_interface` VALUES (12, 'port5', '27.72.28.152', '255.255.255.255', '10.56.239.2', 1, 'WAN', 'static', 'test', 'viettel', 'xxxxxx', 1480, '27.72.28.152', '20:1a:06:96:c5:36', '2020-07-01 15:33:50.069132', '2020-05-23 09:25:15.594962');
INSERT INTO `network_interface` VALUES (14, 'port6', '27.72.28.152', '255.255.255.255', '10.56.239.2', 1, 'WAN', 'PPPoE', 'test', 'viettel', 'xxxxxx', 1480, '27.72.28.152', '20:1a:06:96:c5:36', '2020-05-23 09:26:08.872869', '2020-05-23 09:26:08.872847');
INSERT INTO `network_interface` VALUES (32, 'testtt', '27.72.28.152', '255.255.255.255', '10.56.239.2', 1, 'WAN', 'PPPoE', 'test', 'viettel', 'xxxxxx', 1480, '27.72.28.152', '20:1a:06:96:c5:36', '2020-06-01 09:36:22.019091', '2020-06-01 09:36:22.019081');
INSERT INTO `network_interface` VALUES (33, 'test tiep', '27.72.28.152', '255.255.255.255', '10.56.239.2', 1, 'WAN', 'PPPoE', 'test', 'viettel', 'xxxxxx', 1480, '27.72.28.152', '20:1a:06:96:c5:36', '2020-07-06 14:54:11.271907', '2020-07-06 14:54:11.271897');
INSERT INTO `network_interface` VALUES (35, 'test tiep2', '27.72.28.152', '255.255.255.255', '10.56.239.2', 1, 'WAN', 'abc', NULL, NULL, NULL, NULL, NULL, NULL, '2020-07-10 08:42:03.696957', '2020-07-10 08:42:03.696931');

-- ----------------------------
-- Table structure for network_load_balancing
-- ----------------------------
DROP TABLE IF EXISTS `network_load_balancing`;
CREATE TABLE `network_load_balancing`  (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `status` int(10) NULL DEFAULT NULL,
  `command` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `server` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `timeout` int(10) NULL DEFAULT NULL,
  `threshold` int(10) NULL DEFAULT NULL,
  `interface` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8 COLLATE = utf8_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of network_load_balancing
-- ----------------------------
INSERT INTO `network_load_balancing` VALUES (1, 1, 'ping', '10.56.239.2', 100, 10, '[12, 14]');

-- ----------------------------
-- Table structure for network_nat
-- ----------------------------
DROP TABLE IF EXISTS `network_nat`;
CREATE TABLE `network_nat`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `protocol` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `type` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `ip_address` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `service` int(10) NULL DEFAULT NULL,
  `ip_map` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `port_map` int(10) NULL DEFAULT NULL,
  `status` int(10) NULL DEFAULT NULL,
  `interface` int(11) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `unique_name`(`name`) USING BTREE,
  INDEX `fk_nat_interface`(`interface`) USING BTREE,
  CONSTRAINT `fk_nat_interface` FOREIGN KEY (`interface`) REFERENCES `network_interface` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB AUTO_INCREMENT = 16 CHARACTER SET = utf8 COLLATE = utf8_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of network_nat
-- ----------------------------
INSERT INTO `network_nat` VALUES (11, 'policy edit', '[\'TCP\', \'UDP\']', 'DNAT', '27.72.28.152', 3001, '10.56.239.2', 1003, 1, NULL);
INSERT INTO `network_nat` VALUES (12, 'policy 1', 'TCP,UDP', 'DNAT', '27.72.28.152', 3001, '10.56.239.2', 1003, 1, 12);
INSERT INTO `network_nat` VALUES (15, 'policy 1df', 'TCP,UDP', 'DNAT', '27.72.28.152', 3001, '10.56.239.2', 1003, 1, 12);

-- ----------------------------
-- Table structure for operating_mode
-- ----------------------------
DROP TABLE IF EXISTS `operating_mode`;
CREATE TABLE `operating_mode`  (
  `id` int(10) NOT NULL,
  `mode` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of operating_mode
-- ----------------------------
INSERT INTO `operating_mode` VALUES (1, 'Nat');

-- ----------------------------
-- Table structure for report_schedule
-- ----------------------------
DROP TABLE IF EXISTS `report_schedule`;
CREATE TABLE `report_schedule`  (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `frequency` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `specific_day` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `start_time` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `type` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `email` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 8 CHARACTER SET = utf8 COLLATE = utf8_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of report_schedule
-- ----------------------------
INSERT INTO `report_schedule` VALUES (3, 'report put1', 'monthly', '22', '21/04/2020 02:36:31', '[\'system_report\', \'ad_report\']', '[\'mail1@email.com\', \'mail2@email.com\', \'mail3@email.com\']');
INSERT INTO `report_schedule` VALUES (4, 'report test', 'monthly', '22', '21/04/2020 02:36:31', '[\'system_report\', \'ad_report\']', '[\'mail1@email.com\', \'mail2@email.com\', \'mail3@email.com\']');
INSERT INTO `report_schedule` VALUES (5, 'report test', 'monthly', '22', '21/04/2020 02:36:31', '[\'system_report\', \'ad_report\']', '[\'mail1@email.com\', \'mail2@email.com\', \'mail3@email.com\']');
INSERT INTO `report_schedule` VALUES (6, 'report test', 'monthly', '22', '21/04/2020 02:36:31', '[\'system_report\', \'ad_report\']', '[\'mail1@email.com\', \'mail2@email.com\', \'mail3@email.com\']');
INSERT INTO `report_schedule` VALUES (7, 'report test', 'monthly', '22', '21/04/2020 02:36:31', '[\'system_report\', \'ad_report\']', '[\'mail1@email.com\', \'mail2@email.com\', \'mail3@email.com\']');

-- ----------------------------
-- Table structure for routes
-- ----------------------------
DROP TABLE IF EXISTS `routes`;
CREATE TABLE `routes`  (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `created_at` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `description` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `destination` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `gateway` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `metric` int(10) NULL DEFAULT NULL,
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `netmask` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `status` int(10) NULL DEFAULT NULL,
  `updated_at` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 30 CHARACTER SET = utf8 COLLATE = utf8_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of routes
-- ----------------------------
INSERT INTO `routes` VALUES (29, '2020-07-09 10:53:08.595309', 'abc', '169.196.111.0', '192.168.200.1', 1, 'test add 2', '255.255.255.0', 1, '2020-07-09 10:53:08.595317');

-- ----------------------------
-- Table structure for service
-- ----------------------------
DROP TABLE IF EXISTS `service`;
CREATE TABLE `service`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `port` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `protocol` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `description` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8 COLLATE = utf8_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of service
-- ----------------------------
INSERT INTO `service` VALUES (1, 'Test add', '1234,5678', 'TCP,UDP', 'abc');
INSERT INTO `service` VALUES (2, 'Test edit', '1234,5678', 'TCP,UDP', 'abc');

-- ----------------------------
-- Table structure for signature
-- ----------------------------
DROP TABLE IF EXISTS `signature`;
CREATE TABLE `signature`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `type` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `description` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `content` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `status` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `ad_profile` int(11) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `fk_profile1`(`ad_profile`) USING BTREE,
  CONSTRAINT `fk_profile1` FOREIGN KEY (`ad_profile`) REFERENCES `ad_profile` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8 COLLATE = utf8_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of signature
-- ----------------------------
INSERT INTO `signature` VALUES (1, 'test data', '1', '1', '1', '1', 1);
INSERT INTO `signature` VALUES (2, 'test data', '2', '2', '2', '1', 1);
INSERT INTO `signature` VALUES (3, 'test data', '3', '3', '3', '0', 1);

-- ----------------------------
-- Table structure for system_users
-- ----------------------------
DROP TABLE IF EXISTS `system_users`;
CREATE TABLE `system_users`  (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `username` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT '',
  `avatar` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT '',
  `password` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `username`(`username`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 20 CHARACTER SET = utf8 COLLATE = utf8_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of system_users
-- ----------------------------
INSERT INTO `system_users` VALUES (1, 'khanhkd1', 'Admin1', 'https://picsum.photos/200/200', '123123');
INSERT INTO `system_users` VALUES (17, 'khanhkd2', 'abc', 'https://picsum.photos/200/200', '123123');
INSERT INTO `system_users` VALUES (19, 'khanhkd11', NULL, NULL, 'aaaa');

-- ----------------------------
-- Table structure for tcp_general
-- ----------------------------
DROP TABLE IF EXISTS `tcp_general`;
CREATE TABLE `tcp_general`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `description` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `data` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `status` int(11) NULL DEFAULT 1,
  `input_type` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `input_id` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `member_name` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `member_value` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `profile` int(11) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `tcp_general_ad_profile_id_fk`(`profile`) USING BTREE,
  CONSTRAINT `tcp_general_ad_profile_id_fk` FOREIGN KEY (`profile`) REFERENCES `ad_profile` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB AUTO_INCREMENT = 74 CHARACTER SET = utf8 COLLATE = utf8_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of tcp_general
-- ----------------------------
INSERT INTO `tcp_general` VALUES (1, 'Packet Normalization', 'Kiểm tra bất thường gói tin', '1', 1, 'switch', 'packet_normalization', NULL, NULL, NULL);
INSERT INTO `tcp_general` VALUES (2, 'Anti Spoofed IP', NULL, '1', 1, 'check_box', 'spoofed_ip', 'inb_source,inb_dest,outb_source,outb_dest', '1,1,1,1', NULL);
INSERT INTO `tcp_general` VALUES (3, 'SYN Rate Limiting for Popular TCP', NULL, '1', 1, 'switch', 'syn_rate_tcp', NULL, NULL, NULL);
INSERT INTO `tcp_general` VALUES (4, 'SYN Rate for Other TCP', NULL, '1', 1, 'switch', 'syn_rate_other', NULL, NULL, NULL);
INSERT INTO `tcp_general` VALUES (5, 'SYN Prevention', NULL, '1', 1, 'switch', 'syn_prevention', NULL, NULL, NULL);
INSERT INTO `tcp_general` VALUES (6, 'Block Tor Nodes', NULL, '1', 1, 'switch', 'block_tor', NULL, NULL, NULL);
INSERT INTO `tcp_general` VALUES (7, 'Block Bogon and Unused IP Subnets', NULL, '1', 1, 'switch', 'block_bogon', NULL, NULL, NULL);
INSERT INTO `tcp_general` VALUES (8, 'Reverse Path Checking', NULL, '1', 1, 'switch', 'rev_path_check', NULL, NULL, NULL);
INSERT INTO `tcp_general` VALUES (9, 'Drop UDP Packets', NULL, '1', 1, 'switch', 'drop_udp', NULL, NULL, NULL);
INSERT INTO `tcp_general` VALUES (10, 'ICMP Flood Mitigation', NULL, '1', 1, 'switch', 'icmp_flood_mitigataion', NULL, NULL, NULL);
INSERT INTO `tcp_general` VALUES (11, 'Block IPv6', NULL, '1', 1, 'switch', 'block_ipv6', NULL, NULL, NULL);
INSERT INTO `tcp_general` VALUES (12, 'Geography Blocking', NULL, 'us', 1, 'combo_box', 'geography_block', 'American', 'us', NULL);
INSERT INTO `tcp_general` VALUES (13, 'Ivalid ICMP Anomaly', NULL, '1', 1, 'switch', 'invalid_icmp', NULL, NULL, NULL);
INSERT INTO `tcp_general` VALUES (14, 'Blocking by Identified', NULL, '300', 1, 'input', 'block_ident', NULL, NULL, NULL);
INSERT INTO `tcp_general` VALUES (15, 'Block by Threshold', NULL, '300', 1, 'input', 'block_threshold', NULL, NULL, NULL);
INSERT INTO `tcp_general` VALUES (16, 'Detect Proxy IP by Number of Connections', NULL, '1', 1, 'switch', 'detect_proxy', NULL, NULL, NULL);
INSERT INTO `tcp_general` VALUES (17, 'Proxy IP Threshold', NULL, '10', 1, 'input', 'proxy_threshold', NULL, NULL, NULL);
INSERT INTO `tcp_general` VALUES (18, 'Detect Proxy IP Using Header', NULL, '1', 1, 'switch', 'detect_proxy_header', NULL, NULL, NULL);
INSERT INTO `tcp_general` VALUES (19, 'Detect Proxy IP Using Header', NULL, '1', 1, 'switch', 'detect_proxy_header', NULL, NULL, 13);
INSERT INTO `tcp_general` VALUES (20, 'Packet Normalization', 'Kiểm tra bất thường gói tin', '1', 1, 'switch', 'packet_normalization', NULL, NULL, 14);
INSERT INTO `tcp_general` VALUES (21, 'Anti Spoofed IP', NULL, 'inb_source,inb_dest,outb_source', 1, 'check_box', 'spoofed_ip', 'inb_source,inb_dest,outb_source,outb_dest', 'inb_source,inb_dest,outb_source,outb_dest', 14);
INSERT INTO `tcp_general` VALUES (22, 'SYN Rate Limiting for Popular TCP', NULL, '1', 1, 'switch', 'syn_rate_tcp', NULL, NULL, 14);
INSERT INTO `tcp_general` VALUES (23, 'SYN Rate for Other TCP', NULL, '1', 1, 'switch', 'syn_rate_other', NULL, NULL, 14);
INSERT INTO `tcp_general` VALUES (24, 'SYN Prevention', NULL, '1', 1, 'switch', 'syn_prevention', NULL, NULL, 14);
INSERT INTO `tcp_general` VALUES (25, 'Block Tor Nodes', NULL, '1', 1, 'switch', 'block_tor', NULL, NULL, 14);
INSERT INTO `tcp_general` VALUES (26, 'Block Bogon and Unused IP Subnets', NULL, '1', 1, 'switch', 'block_bogon', NULL, NULL, 14);
INSERT INTO `tcp_general` VALUES (27, 'Reverse Path Checking', NULL, '1', 1, 'switch', 'rev_path_check', NULL, NULL, 14);
INSERT INTO `tcp_general` VALUES (28, 'Drop UDP Packets', NULL, '1', 1, 'switch', 'drop_udp', NULL, NULL, 14);
INSERT INTO `tcp_general` VALUES (29, 'ICMP Flood Mitigation', NULL, '1', 1, 'switch', 'icmp_flood_mitigataion', NULL, NULL, 14);
INSERT INTO `tcp_general` VALUES (30, 'Block IPv6', NULL, '1', 1, 'switch', 'block_ipv6', NULL, NULL, 14);
INSERT INTO `tcp_general` VALUES (31, 'Geography Blocking', NULL, '1', 1, 'combo_box', 'geography_block', 'American', 'us', 14);
INSERT INTO `tcp_general` VALUES (32, 'Ivalid ICMP Anomaly', NULL, '1', 1, 'switch', 'invalid_icmp', NULL, NULL, 14);
INSERT INTO `tcp_general` VALUES (33, 'Blocking by Identified', NULL, '300', 1, 'input', 'block_ident', NULL, NULL, 14);
INSERT INTO `tcp_general` VALUES (34, 'Block by Threshold', NULL, '300', 1, 'input', 'block_threshold', NULL, NULL, 14);
INSERT INTO `tcp_general` VALUES (35, 'Detect Proxy IP by Number of Connections', NULL, '1', 1, 'switch', 'detect_proxy', NULL, NULL, 14);
INSERT INTO `tcp_general` VALUES (36, 'Proxy IP Threshold', NULL, '10', 1, 'input', 'proxy_threshold', NULL, NULL, 14);
INSERT INTO `tcp_general` VALUES (37, 'Detect Proxy IP Using Header', NULL, '1', 1, 'switch', 'detect_proxy_header', NULL, NULL, 14);
INSERT INTO `tcp_general` VALUES (38, 'Packet Normalization', 'Kiểm tra bất thường gói tin', '1', 1, 'switch', 'packet_normalization', NULL, NULL, 15);
INSERT INTO `tcp_general` VALUES (39, 'Anti Spoofed IP', NULL, '1', 1, 'check_box', 'spoofed_ip', 'inb_source,inb_dest,outb_source,outb_dest', '1,1,1,1', 15);
INSERT INTO `tcp_general` VALUES (40, 'SYN Rate Limiting for Popular TCP', NULL, '1', 1, 'switch', 'syn_rate_tcp', NULL, NULL, 15);
INSERT INTO `tcp_general` VALUES (41, 'SYN Rate for Other TCP', NULL, '1', 1, 'switch', 'syn_rate_other', NULL, NULL, 15);
INSERT INTO `tcp_general` VALUES (42, 'SYN Prevention', NULL, '1', 1, 'switch', 'syn_prevention', NULL, NULL, 15);
INSERT INTO `tcp_general` VALUES (43, 'Block Tor Nodes', NULL, '1', 1, 'switch', 'block_tor', NULL, NULL, 15);
INSERT INTO `tcp_general` VALUES (44, 'Block Bogon and Unused IP Subnets', NULL, '1', 1, 'switch', 'block_bogon', NULL, NULL, 15);
INSERT INTO `tcp_general` VALUES (45, 'Reverse Path Checking', NULL, '1', 1, 'switch', 'rev_path_check', NULL, NULL, 15);
INSERT INTO `tcp_general` VALUES (46, 'Drop UDP Packets', NULL, '1', 1, 'switch', 'drop_udp', NULL, NULL, 15);
INSERT INTO `tcp_general` VALUES (47, 'ICMP Flood Mitigation', NULL, '1', 1, 'switch', 'icmp_flood_mitigataion', NULL, NULL, 15);
INSERT INTO `tcp_general` VALUES (48, 'Block IPv6', NULL, '1', 1, 'switch', 'block_ipv6', NULL, NULL, 15);
INSERT INTO `tcp_general` VALUES (49, 'Geography Blocking', NULL, '1', 1, 'combo_box', 'geography_block', 'American', 'us', 15);
INSERT INTO `tcp_general` VALUES (50, 'Ivalid ICMP Anomaly', NULL, '1', 1, 'switch', 'invalid_icmp', NULL, NULL, 15);
INSERT INTO `tcp_general` VALUES (51, 'Blocking by Identified', NULL, '300', 1, 'input', 'block_ident', NULL, NULL, 15);
INSERT INTO `tcp_general` VALUES (52, 'Block by Threshold', NULL, '300', 1, 'input', 'block_threshold', NULL, NULL, 15);
INSERT INTO `tcp_general` VALUES (53, 'Detect Proxy IP by Number of Connections', NULL, '1', 1, 'switch', 'detect_proxy', NULL, NULL, 15);
INSERT INTO `tcp_general` VALUES (54, 'Proxy IP Threshold', NULL, '10', 1, 'input', 'proxy_threshold', NULL, NULL, 15);
INSERT INTO `tcp_general` VALUES (55, 'Detect Proxy IP Using Header', NULL, '1', 1, 'switch', 'detect_proxy_header', NULL, NULL, 15);
INSERT INTO `tcp_general` VALUES (56, 'Packet Normalization', 'Kiểm tra bất thường gói tin', '1', 1, 'switch', 'packet_normalization', NULL, NULL, 16);
INSERT INTO `tcp_general` VALUES (57, 'Anti Spoofed IP', NULL, '1', 1, 'check_box', 'spoofed_ip', 'inb_source,inb_dest,outb_source,outb_dest', '1,1,1,1', 16);
INSERT INTO `tcp_general` VALUES (58, 'SYN Rate Limiting for Popular TCP', NULL, '1', 1, 'switch', 'syn_rate_tcp', NULL, NULL, 16);
INSERT INTO `tcp_general` VALUES (59, 'SYN Rate for Other TCP', NULL, '1', 1, 'switch', 'syn_rate_other', NULL, NULL, 16);
INSERT INTO `tcp_general` VALUES (60, 'SYN Prevention', NULL, '1', 1, 'switch', 'syn_prevention', NULL, NULL, 16);
INSERT INTO `tcp_general` VALUES (61, 'Block Tor Nodes', NULL, '1', 1, 'switch', 'block_tor', NULL, NULL, 16);
INSERT INTO `tcp_general` VALUES (62, 'Block Bogon and Unused IP Subnets', NULL, '1', 1, 'switch', 'block_bogon', NULL, NULL, 16);
INSERT INTO `tcp_general` VALUES (63, 'Reverse Path Checking', NULL, '1', 1, 'switch', 'rev_path_check', NULL, NULL, 16);
INSERT INTO `tcp_general` VALUES (64, 'Drop UDP Packets', NULL, '1', 1, 'switch', 'drop_udp', NULL, NULL, 16);
INSERT INTO `tcp_general` VALUES (65, 'ICMP Flood Mitigation', NULL, '1', 1, 'switch', 'icmp_flood_mitigataion', NULL, NULL, 16);
INSERT INTO `tcp_general` VALUES (66, 'Block IPv6', NULL, '1', 1, 'switch', 'block_ipv6', NULL, NULL, 16);
INSERT INTO `tcp_general` VALUES (67, 'Geography Blocking', NULL, '1', 1, 'combo_box', 'geography_block', 'American', 'us', 16);
INSERT INTO `tcp_general` VALUES (68, 'Ivalid ICMP Anomaly', NULL, '1', 1, 'switch', 'invalid_icmp', NULL, NULL, 16);
INSERT INTO `tcp_general` VALUES (69, 'Blocking by Identified', NULL, '300', 1, 'input', 'block_ident', NULL, NULL, 16);
INSERT INTO `tcp_general` VALUES (70, 'Block by Threshold', NULL, '300', 1, 'input', 'block_threshold', NULL, NULL, 16);
INSERT INTO `tcp_general` VALUES (71, 'Detect Proxy IP by Number of Connections', NULL, '1', 1, 'switch', 'detect_proxy', NULL, NULL, 16);
INSERT INTO `tcp_general` VALUES (72, 'Proxy IP Threshold', NULL, '10', 1, 'input', 'proxy_threshold', NULL, NULL, 16);
INSERT INTO `tcp_general` VALUES (73, 'Detect Proxy IP Using Header', NULL, '1', 1, 'switch', 'detect_proxy_header', NULL, NULL, 16);

-- ----------------------------
-- Table structure for tcp_general_def
-- ----------------------------
DROP TABLE IF EXISTS `tcp_general_def`;
CREATE TABLE `tcp_general_def`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `description` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `data` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `status` int(11) NULL DEFAULT 1,
  `input_type` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `input_id` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `member_name` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `member_value` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 19 CHARACTER SET = utf8 COLLATE = utf8_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of tcp_general_def
-- ----------------------------
INSERT INTO `tcp_general_def` VALUES (1, 'Packet Normalization', 'Kiểm tra bất thường gói tin', '1', 1, 'switch', 'packet_normalization', NULL, NULL);
INSERT INTO `tcp_general_def` VALUES (2, 'Anti Spoofed IP', NULL, '1', 1, 'check_box', 'spoofed_ip', 'inb_source,inb_dest,outb_source,outb_dest', '1,1,1,1');
INSERT INTO `tcp_general_def` VALUES (3, 'SYN Rate Limiting for Popular TCP', NULL, '1', 1, 'switch', 'syn_rate_tcp', NULL, NULL);
INSERT INTO `tcp_general_def` VALUES (4, 'SYN Rate for Other TCP', NULL, '1', 1, 'switch', 'syn_rate_other', NULL, NULL);
INSERT INTO `tcp_general_def` VALUES (5, 'SYN Prevention', NULL, '1', 1, 'switch', 'syn_prevention', NULL, NULL);
INSERT INTO `tcp_general_def` VALUES (6, 'Block Tor Nodes', NULL, '1', 1, 'switch', 'block_tor', NULL, NULL);
INSERT INTO `tcp_general_def` VALUES (7, 'Block Bogon and Unused IP Subnets', NULL, '1', 1, 'switch', 'block_bogon', NULL, NULL);
INSERT INTO `tcp_general_def` VALUES (8, 'Reverse Path Checking', NULL, '1', 1, 'switch', 'rev_path_check', NULL, NULL);
INSERT INTO `tcp_general_def` VALUES (9, 'Drop UDP Packets', NULL, '1', 1, 'switch', 'drop_udp', NULL, NULL);
INSERT INTO `tcp_general_def` VALUES (10, 'ICMP Flood Mitigation', NULL, '1', 1, 'switch', 'icmp_flood_mitigataion', NULL, NULL);
INSERT INTO `tcp_general_def` VALUES (11, 'Block IPv6', NULL, '1', 1, 'switch', 'block_ipv6', NULL, NULL);
INSERT INTO `tcp_general_def` VALUES (12, 'Geography Blocking', NULL, '1', 1, 'combo_box', 'geography_block', 'American', 'us');
INSERT INTO `tcp_general_def` VALUES (13, 'Ivalid ICMP Anomaly', NULL, '1', 1, 'switch', 'invalid_icmp', NULL, NULL);
INSERT INTO `tcp_general_def` VALUES (14, 'Blocking by Identified', NULL, '300', 1, 'input', 'block_ident', NULL, NULL);
INSERT INTO `tcp_general_def` VALUES (15, 'Block by Threshold', NULL, '300', 1, 'input', 'block_threshold', NULL, NULL);
INSERT INTO `tcp_general_def` VALUES (16, 'Detect Proxy IP by Number of Connections', NULL, '1', 1, 'switch', 'detect_proxy', NULL, NULL);
INSERT INTO `tcp_general_def` VALUES (17, 'Proxy IP Threshold', NULL, '10', 1, 'input', 'proxy_threshold', NULL, NULL);
INSERT INTO `tcp_general_def` VALUES (18, 'Detect Proxy IP Using Header', NULL, '1', 1, 'switch', 'detect_proxy_header', NULL, NULL);

-- ----------------------------
-- Table structure for tcp_slowcnn
-- ----------------------------
DROP TABLE IF EXISTS `tcp_slowcnn`;
CREATE TABLE `tcp_slowcnn`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `description` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `data` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `status` int(11) NULL DEFAULT 1,
  `input_type` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `input_id` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `member_name` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `member_value` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `profile` int(11) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `tcp_slowcnn_ad_profile_id_fk`(`profile`) USING BTREE,
  CONSTRAINT `tcp_slowcnn_ad_profile_id_fk` FOREIGN KEY (`profile`) REFERENCES `ad_profile` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB AUTO_INCREMENT = 11 CHARACTER SET = utf8 COLLATE = utf8_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of tcp_slowcnn
-- ----------------------------
INSERT INTO `tcp_slowcnn` VALUES (1, 'Slow TCP Connections', NULL, '1', 1, 'switch', 'slow_tcp', NULL, NULL, NULL);
INSERT INTO `tcp_slowcnn` VALUES (2, 'High Concurrent Connection per Source', NULL, '1', 1, 'switch', 'hight_cnn', NULL, NULL, NULL);
INSERT INTO `tcp_slowcnn` VALUES (3, 'Byte Threshold', 'Payload in bytes', '100', 1, 'input', 'bytes_payload', NULL, NULL, NULL);
INSERT INTO `tcp_slowcnn` VALUES (4, 'Observation Period', 'In Seconds', '100', 1, 'input', 'ob_period', NULL, NULL, NULL);
INSERT INTO `tcp_slowcnn` VALUES (5, 'Block Source with Slow Connection', NULL, '1', 1, 'switch', 'block_source_slowcnn', NULL, NULL, NULL);
INSERT INTO `tcp_slowcnn` VALUES (6, 'Slow TCP Connections', NULL, '1', 0, 'switch', 'slow_tcp', NULL, NULL, 16);
INSERT INTO `tcp_slowcnn` VALUES (7, 'High Concurrent Connection per Source', NULL, '1', 1, 'switch', 'hight_cnn', NULL, NULL, 16);
INSERT INTO `tcp_slowcnn` VALUES (8, 'Byte Threshold', 'Payload in bytes', '100', 1, 'input', 'bytes_payload', NULL, NULL, 16);
INSERT INTO `tcp_slowcnn` VALUES (9, 'Observation Period', 'In Seconds', '100', 1, 'input', 'ob_period', NULL, NULL, 16);
INSERT INTO `tcp_slowcnn` VALUES (10, 'Block Source with Slow Connection', NULL, '1', 1, 'switch', 'block_source_slowcnn', NULL, NULL, 16);

-- ----------------------------
-- Table structure for tcp_slowcnn_def
-- ----------------------------
DROP TABLE IF EXISTS `tcp_slowcnn_def`;
CREATE TABLE `tcp_slowcnn_def`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `description` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `data` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `status` int(11) NULL DEFAULT 1,
  `input_type` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `input_id` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `member_name` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `member_value` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `profile` int(11) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 6 CHARACTER SET = utf8 COLLATE = utf8_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of tcp_slowcnn_def
-- ----------------------------
INSERT INTO `tcp_slowcnn_def` VALUES (1, 'Slow TCP Connections', NULL, '1', 1, 'switch', 'slow_tcp', NULL, NULL, NULL);
INSERT INTO `tcp_slowcnn_def` VALUES (2, 'High Concurrent Connection per Source', NULL, '1', 1, 'switch', 'hight_cnn', NULL, NULL, NULL);
INSERT INTO `tcp_slowcnn_def` VALUES (3, 'Byte Threshold', 'Payload in bytes', '100', 1, 'input', 'bytes_payload', NULL, NULL, NULL);
INSERT INTO `tcp_slowcnn_def` VALUES (4, 'Observation Period', 'In Seconds', '100', 1, 'input', 'ob_period', NULL, NULL, NULL);
INSERT INTO `tcp_slowcnn_def` VALUES (5, 'Block Source with Slow Connection', NULL, '1', 1, 'switch', 'block_source_slowcnn', NULL, NULL, NULL);

-- ----------------------------
-- Table structure for tcp_threshold
-- ----------------------------
DROP TABLE IF EXISTS `tcp_threshold`;
CREATE TABLE `tcp_threshold`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `packet_in` int(11) NULL DEFAULT NULL,
  `packet_out` int(11) NULL DEFAULT NULL,
  `bandwidth_in` int(11) NULL DEFAULT NULL,
  `bandwidth_out` int(11) NULL DEFAULT NULL,
  `percent` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `description` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `prevention` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `status` int(11) NULL DEFAULT NULL,
  `type` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `profile` int(11) NULL DEFAULT NULL,
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `tcp_threshold_ad_profile_id_fk`(`profile`) USING BTREE,
  CONSTRAINT `tcp_threshold_ad_profile_id_fk` FOREIGN KEY (`profile`) REFERENCES `ad_profile` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB AUTO_INCREMENT = 7 CHARACTER SET = utf8 COLLATE = utf8_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of tcp_threshold
-- ----------------------------
INSERT INTO `tcp_threshold` VALUES (3, 100, 100, 100, 100, '20.7', 'abc', 'drop', 1, 'protocol', 2, 'test add');
INSERT INTO `tcp_threshold` VALUES (4, 100, 100, 100, 100, '20.7', 'abc', 'drop', 1, 'protocol', 2, 'test edit 123');

-- ----------------------------
-- Table structure for tcp_threshold_have_groupnetworks
-- ----------------------------
DROP TABLE IF EXISTS `tcp_threshold_have_groupnetworks`;
CREATE TABLE `tcp_threshold_have_groupnetworks`  (
  `tcp_threshold_id` int(11) NOT NULL,
  `group_network_id` int(11) NOT NULL,
  PRIMARY KEY (`tcp_threshold_id`, `group_network_id`) USING BTREE,
  INDEX `tcp_threshold_have_groupnetworks_group_network_id_fk`(`group_network_id`) USING BTREE,
  CONSTRAINT `tcp_threshold_have_groupnetworks_group_network_id_fk` FOREIGN KEY (`group_network_id`) REFERENCES `group_network` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `tcp_threshold_have_groupnetworks_tcp_threshold_id_fk` FOREIGN KEY (`tcp_threshold_id`) REFERENCES `tcp_threshold` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of tcp_threshold_have_groupnetworks
-- ----------------------------

-- ----------------------------
-- Table structure for tcp_threshold_have_groupservices
-- ----------------------------
DROP TABLE IF EXISTS `tcp_threshold_have_groupservices`;
CREATE TABLE `tcp_threshold_have_groupservices`  (
  `tcp_threshold_id` int(11) NOT NULL,
  `group_service_id` int(11) NOT NULL,
  PRIMARY KEY (`tcp_threshold_id`, `group_service_id`) USING BTREE,
  INDEX `tcp_threshold_have_groupservices_group_service_id_fk`(`group_service_id`) USING BTREE,
  CONSTRAINT `tcp_threshold_have_groupservices_group_service_id_fk` FOREIGN KEY (`group_service_id`) REFERENCES `group_service` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `tcp_threshold_have_groupservices_tcp_threshold_id_fk` FOREIGN KEY (`tcp_threshold_id`) REFERENCES `tcp_threshold` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of tcp_threshold_have_groupservices
-- ----------------------------
INSERT INTO `tcp_threshold_have_groupservices` VALUES (4, 3);

-- ----------------------------
-- Table structure for tcp_threshold_have_networks
-- ----------------------------
DROP TABLE IF EXISTS `tcp_threshold_have_networks`;
CREATE TABLE `tcp_threshold_have_networks`  (
  `tcp_threshold_id` int(11) NOT NULL,
  `network_id` int(11) NOT NULL,
  PRIMARY KEY (`tcp_threshold_id`, `network_id`) USING BTREE,
  INDEX `fk_network_id69`(`network_id`) USING BTREE,
  CONSTRAINT `fk_network_id69` FOREIGN KEY (`network_id`) REFERENCES `network` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_tcp_threshold_id69` FOREIGN KEY (`tcp_threshold_id`) REFERENCES `tcp_threshold` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of tcp_threshold_have_networks
-- ----------------------------

-- ----------------------------
-- Table structure for tcp_threshold_have_services
-- ----------------------------
DROP TABLE IF EXISTS `tcp_threshold_have_services`;
CREATE TABLE `tcp_threshold_have_services`  (
  `tcp_threshold_id` int(11) NOT NULL,
  `service_id` int(11) NOT NULL,
  PRIMARY KEY (`tcp_threshold_id`, `service_id`) USING BTREE,
  INDEX `tcp_threshold_have_services_service_id_fk`(`service_id`) USING BTREE,
  CONSTRAINT `tcp_threshold_have_services_service_id_fk` FOREIGN KEY (`service_id`) REFERENCES `service` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `tcp_threshold_have_services_tcp_threshold_id_fk` FOREIGN KEY (`tcp_threshold_id`) REFERENCES `tcp_threshold` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of tcp_threshold_have_services
-- ----------------------------
INSERT INTO `tcp_threshold_have_services` VALUES (3, 1);
INSERT INTO `tcp_threshold_have_services` VALUES (4, 1);
INSERT INTO `tcp_threshold_have_services` VALUES (3, 2);

-- ----------------------------
-- Table structure for virtual_interface
-- ----------------------------
DROP TABLE IF EXISTS `virtual_interface`;
CREATE TABLE `virtual_interface`  (
  `interface_name` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `is_enable` int(10) NULL DEFAULT NULL,
  `virtual_ip_address` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `priority` int(10) NULL DEFAULT NULL,
  PRIMARY KEY (`interface_name`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of virtual_interface
-- ----------------------------
INSERT INTO `virtual_interface` VALUES ('port0', 0, '192.168.0.30', 100);
INSERT INTO `virtual_interface` VALUES ('port2', 1, '192.168.20.100', 20);

-- ----------------------------
-- Table structure for websites
-- ----------------------------
DROP TABLE IF EXISTS `websites`;
CREATE TABLE `websites`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `domain` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `ip_address` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `port` int(255) NULL DEFAULT NULL,
  `listen_port` int(255) NULL DEFAULT NULL,
  `ssl` int(255) NULL DEFAULT NULL,
  `cache` int(255) NULL DEFAULT NULL,
  `key` text CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL,
  `cert` text CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL,
  `status` int(255) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 14 CHARACTER SET = utf8 COLLATE = utf8_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of websites
-- ----------------------------
INSERT INTO `websites` VALUES (5, 'bkav.com.vn', '10.2.32.113', 443, 443, 1, 1, '', '', 1);
INSERT INTO `websites` VALUES (6, 'bkav.com.vn', '10.2.32.113', 443, 443, 1, 1, '', '', 1);
INSERT INTO `websites` VALUES (8, 'bkav.com.vn', '10.2.32.113', 443, 443, 1, 1, '', '', 1);
INSERT INTO `websites` VALUES (10, 'bkav.com.vn', '10.2.32.113', 443, 443, 1, 1, '', '', 1);
INSERT INTO `websites` VALUES (11, 'bkav.com.vn', '10.2.32.113', 443, 443, 1, 1, '1321dsew3232', '', 1);
INSERT INTO `websites` VALUES (12, 'bkav.com.vn', '10.2.32.113', 443, 443, 1, 1, '', '', 1);
INSERT INTO `websites` VALUES (13, 'bkav.com.vn', '10.2.32.113', 443, 443, 1, 1, '', '', 1);

SET FOREIGN_KEY_CHECKS = 1;
