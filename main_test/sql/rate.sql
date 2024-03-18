/*
 Navicat Premium Data Transfer

 Source Server         : admin
 Source Server Type    : MySQL
 Source Server Version : 80026
 Source Host           : localhost:3308
 Source Schema         : rate_408

 Target Server Type    : MySQL
 Target Server Version : 80026
 File Encoding         : 65001

 Date: 18/03/2024 21:11:58
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for rate
-- ----------------------------
DROP TABLE IF EXISTS `rate`;
CREATE TABLE `rate`  (
  `time` datetime NULL DEFAULT NULL COMMENT '时间',
  `chapter` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '章节',
  `q_num` int NULL DEFAULT NULL COMMENT '做题量',
  `error_num` int NULL DEFAULT NULL COMMENT '错题量',
  `correct_rate` double NULL DEFAULT NULL COMMENT '正确率'
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of rate
-- ----------------------------
INSERT INTO `rate` VALUES ('2024-03-18 21:02:48', '6.3.4', 18, 3, 0.83);
INSERT INTO `rate` VALUES ('2024-03-16 21:04:30', '6.2.6', 18, 0, 1);

SET FOREIGN_KEY_CHECKS = 1;
