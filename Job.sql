/*
 Navicat Premium Data Transfer

 Source Server         : 本地库
 Source Server Type    : MySQL
 Source Server Version : 80300 (8.3.0)
 Source Host           : 127.0.0.1:3306
 Source Schema         : Job

 Target Server Type    : MySQL
 Target Server Version : 80300 (8.3.0)
 File Encoding         : 65001

 Date: 13/05/2024 18:11:43
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for class
-- ----------------------------
DROP TABLE IF EXISTS `class`;
CREATE TABLE `class` (
  `id` varchar(36) NOT NULL,
  `class_name` varchar(40) NOT NULL,
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Table structure for resume
-- ----------------------------
DROP TABLE IF EXISTS `resume`;
CREATE TABLE `resume` (
  `account` varchar(30) NOT NULL,
  `name` varchar(255) NOT NULL,
  `phone` varchar(255) NOT NULL,
  `education` varchar(255) NOT NULL,
  `major` varchar(255) NOT NULL,
  `work` varchar(255) NOT NULL,
  `city` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `skill` varchar(255) DEFAULT NULL,
  `award` varchar(255) DEFAULT NULL,
  `practice` varchar(255) DEFAULT NULL,
  `salary` varchar(255) NOT NULL,
  `image` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `gender` varchar(255) NOT NULL,
  `birth` datetime NOT NULL,
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `is_worked` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`account`),
  CONSTRAINT `resume_account` FOREIGN KEY (`account`) REFERENCES `user` (`account`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Table structure for session
-- ----------------------------
DROP TABLE IF EXISTS `session`;
CREATE TABLE `session` (
  `id` varchar(36) NOT NULL,
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `company_name` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `student` varchar(30) NOT NULL,
  `is_read` int NOT NULL DEFAULT '0',
  `work_id` varchar(36) NOT NULL,
  `work_name` varchar(255) NOT NULL,
  `status` int NOT NULL DEFAULT '0',
  `place` varchar(255) DEFAULT NULL,
  `date` datetime DEFAULT NULL,
  `company_id` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`id`),
  KEY `work_id` (`work_id`),
  KEY `work_resume` (`work_name`),
  KEY `student_cons` (`student`),
  KEY `company_name` (`company_name`),
  KEY `company_id` (`company_id`),
  CONSTRAINT `company_id` FOREIGN KEY (`company_id`) REFERENCES `user` (`account`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `company_name` FOREIGN KEY (`company_name`) REFERENCES `user` (`username`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `student_cons` FOREIGN KEY (`student`) REFERENCES `user` (`account`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `work_id` FOREIGN KEY (`work_id`) REFERENCES `work` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `work_resume` FOREIGN KEY (`work_name`) REFERENCES `work` (`title`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Table structure for student_job
-- ----------------------------
DROP TABLE IF EXISTS `student_job`;
CREATE TABLE `student_job` (
  `id` varchar(36) NOT NULL,
  `student` varchar(30) NOT NULL,
  `company_name` varchar(30) NOT NULL,
  `work_name` varchar(30) NOT NULL,
  `city` varchar(50) NOT NULL,
  `salary` int NOT NULL,
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `work` varchar(30) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `student_job` (`student`),
  CONSTRAINT `student_job` FOREIGN KEY (`student`) REFERENCES `user` (`account`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Table structure for test
-- ----------------------------
DROP TABLE IF EXISTS `test`;
CREATE TABLE `test` (
  `id` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Table structure for token
-- ----------------------------
DROP TABLE IF EXISTS `token`;
CREATE TABLE `token` (
  `id` varchar(36) NOT NULL,
  `account` varchar(30) NOT NULL,
  `token` text NOT NULL,
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `user_token` (`account`),
  CONSTRAINT `user_token` FOREIGN KEY (`account`) REFERENCES `user` (`account`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `account` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `username` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `passwd` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `phone` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `email` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `introduce` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `user_type` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `token` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `image` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `is_delete` int NOT NULL DEFAULT '0',
  `is_active` int NOT NULL DEFAULT '1',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `class_id` varchar(36) DEFAULT NULL,
  PRIMARY KEY (`account`) USING BTREE,
  UNIQUE KEY `username` (`username`) USING BTREE,
  UNIQUE KEY `phone` (`phone`) USING BTREE,
  UNIQUE KEY `mail` (`email`) USING BTREE,
  KEY `user_type` (`user_type`),
  KEY `class_id` (`class_id`),
  CONSTRAINT `class_id` FOREIGN KEY (`class_id`) REFERENCES `class` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;

-- ----------------------------
-- Table structure for work
-- ----------------------------
DROP TABLE IF EXISTS `work`;
CREATE TABLE `work` (
  `title` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `education` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `major` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `work` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `city` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `welfare` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `responsibility` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `requirement` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `image` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `salary` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `id` varchar(36) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `visited` int NOT NULL DEFAULT '1',
  `company_name` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `company_id` varchar(30) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  KEY `title` (`title`),
  KEY `work_company_id` (`company_id`),
  KEY `work_name` (`company_name`),
  CONSTRAINT `work_company_id` FOREIGN KEY (`company_id`) REFERENCES `user` (`account`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `work_name` FOREIGN KEY (`company_name`) REFERENCES `user` (`username`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;

-- ----------------------------
-- Triggers structure for table class
-- ----------------------------
DROP TRIGGER IF EXISTS `class_id`;
delimiter ;;
CREATE TRIGGER `class_id` BEFORE INSERT ON `class` FOR EACH ROW BEGIN
    SET NEW.id = UUID();
END
;;
delimiter ;

-- ----------------------------
-- Triggers structure for table session
-- ----------------------------
DROP TRIGGER IF EXISTS `message_uuid`;
delimiter ;;
CREATE TRIGGER `message_uuid` BEFORE INSERT ON `session` FOR EACH ROW BEGIN SET NEW.id = UUID();
END
;;
delimiter ;

-- ----------------------------
-- Triggers structure for table student_job
-- ----------------------------
DROP TRIGGER IF EXISTS `student_job_id`;
delimiter ;;
CREATE TRIGGER `student_job_id` BEFORE INSERT ON `student_job` FOR EACH ROW BEGIN SET NEW.id = UUID();
END
;;
delimiter ;

-- ----------------------------
-- Triggers structure for table token
-- ----------------------------
DROP TRIGGER IF EXISTS `set_token_uuid`;
delimiter ;;
CREATE TRIGGER `set_token_uuid` BEFORE INSERT ON `token` FOR EACH ROW BEGIN SET NEW.id = UUID();
END
;;
delimiter ;

-- ----------------------------
-- Triggers structure for table work
-- ----------------------------
DROP TRIGGER IF EXISTS `set_work_uuid`;
delimiter ;;
CREATE TRIGGER `set_work_uuid` BEFORE INSERT ON `work` FOR EACH ROW BEGIN
    SET NEW.id = UUID();
END
;;
delimiter ;

SET FOREIGN_KEY_CHECKS = 1;
