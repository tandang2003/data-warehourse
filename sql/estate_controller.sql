/*
 Navicat Premium Data Transfer

 Source Server         : dw
 Source Server Type    : MySQL
 Source Server Version : 80040
 Source Host           : localhost:3306
 Source Schema         : estate_controller

 Target Server Type    : MySQL
 Target Server Version : 80040
 File Encoding         : 65001

 Date: 10/12/2024 09:11:52
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for config_databases
-- ----------------------------
DROP TABLE IF EXISTS `config_databases`;
CREATE TABLE `config_databases`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `type_database_id` bigint NULL DEFAULT NULL,
  `host` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `port` int NULL DEFAULT NULL,
  `username` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `password` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `rdbms_type` enum('MYSQL','MONGODB','POSTGRESQL') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `config_databases_type_databases_id_fk`(`type_database_id` ASC) USING BTREE,
  CONSTRAINT `config_databases_type_databases_id_fk` FOREIGN KEY (`type_database_id`) REFERENCES `type_databases` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of config_databases
-- ----------------------------
INSERT INTO `config_databases` VALUES (1, 'estate_staging', 1, '127.0.0.1', 3306, 'estate_root', '1234', 'MYSQL');
INSERT INTO `config_databases` VALUES (2, 'estate_warehouse', 2, '127.0.0.1', 3306, 'estate_root', '1234', 'MYSQL');

-- ----------------------------
-- Table structure for configs
-- ----------------------------
DROP TABLE IF EXISTS `configs`;
CREATE TABLE `configs`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `prefix` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `prefix_error` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `file_format` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `file_extension` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `data_dir_path` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `error_dir_path` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `active` bit(1) NULL DEFAULT b'0',
  `config_database_id` bigint NULL DEFAULT NULL,
  `resource_id` bigint NULL DEFAULT NULL,
  `email` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `configs_config_databases_id_fk`(`config_database_id` ASC) USING BTREE,
  CONSTRAINT `configs_config_databases_id_fk` FOREIGN KEY (`config_database_id`) REFERENCES `config_databases` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 5 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of configs
-- ----------------------------
INSERT INTO `configs` VALUES (1, 'source_1_', 'source_1_error_', '%Y_%m_%d__%H_%M', 'csv', 'D:\\pycharm\\data', 'D:\\pycharm\\error', b'1', 1, 1, '21130171@st.hcmuef.edu.vn');
INSERT INTO `configs` VALUES (2, 'source_2_', 'source_2_error_', '%Y_%m_%d__%H_%M', 'csv', 'D:\\pycharm\\data', 'D:\\pycharm\\error', b'1', 1, 2, '21130171@st.hcmuef.edu.vn');

-- ----------------------------
-- Table structure for logs
-- ----------------------------
DROP TABLE IF EXISTS `logs`;
CREATE TABLE `logs`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `process_id` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `config_id` bigint NULL DEFAULT NULL,
  `status` enum('FILE_PENDING','FILE_ERROR','STAGING_PENDING','WAREHOUSE_PENDING','SUCCESS','STAGING_ERROR','WAREHOUSE_ERROR','DATAMART_ERROR','FILE_PROCESSING','STAGING_PROCESSING','WAREHOUSE_PROCESSING','DATAMART_PROCESSING') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `time_start` datetime NULL DEFAULT NULL,
  `time_end` datetime NULL DEFAULT NULL,
  `file_name` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `error_file_name` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `count_row` int NULL DEFAULT NULL,
  `create_at` datetime NULL DEFAULT NULL,
  `is_delete` tinyint(1) NULL DEFAULT 0,
  `again` bit(1) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `config_id_idx`(`config_id` ASC) USING BTREE,
  CONSTRAINT `logs_ibfk_1` FOREIGN KEY (`config_id`) REFERENCES `configs` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 83 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of logs
-- ----------------------------
INSERT INTO `logs` VALUES (1, NULL, 1, 'FILE_PENDING', '2024-11-14 08:30:00', NULL, 'file1.csv', NULL, 100, '2024-11-20 00:00:00', 1, NULL);
INSERT INTO `logs` VALUES (2, NULL, 2, 'FILE_PENDING', '2024-11-21 08:30:00', NULL, '', NULL, 100, '2024-12-03 00:00:00', 0, NULL);
INSERT INTO `logs` VALUES (74, NULL, 1, 'FILE_PENDING', '2024-12-09 00:37:53', NULL, ' ', ' ', 0, '2024-12-09 00:37:53', 1, NULL);
INSERT INTO `logs` VALUES (75, NULL, 2, 'FILE_PENDING', '2024-12-09 00:37:53', NULL, ' ', ' ', 0, '2024-12-09 00:37:53', 1, NULL);
INSERT INTO `logs` VALUES (78, NULL, 1, 'FILE_PENDING', '2024-12-09 03:00:01', NULL, ' ', ' ', 0, '2024-12-09 03:00:01', 1, NULL);
INSERT INTO `logs` VALUES (79, NULL, 2, 'FILE_PENDING', '2024-12-09 03:00:01', NULL, ' ', ' ', 0, '2024-12-09 03:00:01', 1, NULL);
INSERT INTO `logs` VALUES (80, NULL, 1, 'FILE_PROCESSING', '2024-12-09 03:04:34', '2024-12-09 04:25:47', 'D:\\pycharm\\data\\source_1_2024_12_09__04_25.csv', NULL, 400, '2024-12-09 03:04:34', 1, NULL);
INSERT INTO `logs` VALUES (81, NULL, 1, 'STAGING_PENDING', '2024-12-09 04:25:47', NULL, ' ', ' ', 0, '2024-12-09 04:25:47', 0, NULL);

-- ----------------------------
-- Table structure for resources
-- ----------------------------
DROP TABLE IF EXISTS `resources`;
CREATE TABLE `resources`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `base_url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `source_page` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `paging_pattern` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `limit_page` int NULL DEFAULT NULL,
  `scenario` json NULL,
  `navigate_scenario` json NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of resources
-- ----------------------------
INSERT INTO `resources` VALUES (1, 'batdongsan.com.vn', 'https://batdongsan.com.vn', 'nha-dat-ban', '/p', 20, '{\"nk\": {\"method\": \"get_attribute\", \"quantity\": 1, \"selector\": \"//*[@id=\'product-detail-web\']\", \"attribute\": \"prid\"}, \"url\": {\"method\": \"url\"}, \"area\": {\"method\": \"text\", \"quantity\": 1, \"selector\": \"//*[contains(@class, \'js__pr-short-info-item\')]/*[text()=\'Diện tích\']/following-sibling::*[1]\"}, \"email\": {\"method\": \"get_attribute\", \"quantity\": 1, \"selector\": \"//*[@id=\'email\']\", \"attribute\": \"data-email\"}, \"legal\": {\"method\": \"text\", \"quantity\": 1, \"selector\": \"//*[contains(@class, \'re__pr-specs-content-item\')]/*[text()=\'Pháp lý\']/following-sibling::*[1]\"}, \"price\": {\"method\": \"text\", \"quantity\": 1, \"selector\": \"//*[contains(@class, \'js__pr-short-info-item\')]/*[text()=\'Mức giá\']/following-sibling::*[1]\"}, \"avatar\": {\"method\": \"get_attribute\", \"quantity\": 1, \"selector\": \"//*[contains(@class, \'js__agent-contact-avatar\')]\", \"attribute\": \"src\"}, \"floors\": {\"method\": \"text\", \"quantity\": 1, \"selector\": \"//*[contains(@class, \'re__pr-specs-content-item\')]/*[text()=\'Số tầng\']/following-sibling::*[1]\"}, \"images\": {\"method\": \"get_attribute\", \"quantity\": null, \"selector\": \"//*[contains(@class, \'slick-track\')]//img\", \"attribute\": \"src\"}, \"address\": {\"method\": \"text\", \"quantity\": 1, \"selector\": \"//*[contains(@class, \'js__pr-address\')]\"}, \"bedroom\": {\"method\": \"text\", \"quantity\": 1, \"selector\": \"//*[contains(@class, \'re__pr-specs-content-item\')]/*[text()=\'Số phòng ngủ\']/following-sibling::*[1]\"}, \"subject\": {\"method\": \"text\", \"quantity\": 1, \"selector\": \"//*[contains(@class, \'pr-title\')]\"}, \"bathroom\": {\"method\": \"text\", \"quantity\": 1, \"selector\": \"//*[contains(@class, \'re__pr-specs-content-item\')]/*[text()=\'Số toilet\']/following-sibling::*[1]\"}, \"end_date\": {\"method\": \"text\", \"quantity\": 1, \"selector\": \"//*[contains(@class, \'js__pr-config-item\')]/*[text()=\'Ngày hết hạn\']/following-sibling::*[1]\"}, \"create_at\": {\"method\": \"time\"}, \"full_name\": {\"method\": \"get_attribute\", \"quantity\": 1, \"selector\": \"(//*[contains(@class, \'js_contact-name\')])[1]\", \"attribute\": \"title\"}, \"start_date\": {\"method\": \"text\", \"quantity\": 1, \"selector\": \"//*[contains(@class, \'js__pr-config-item\')]/*[text()=\'Ngày đăng\']/following-sibling::*[1]\"}, \"description\": {\"method\": \"description\", \"selector\": \"//*[contains(@class, \'re__detail-content\')]\"}, \"orientation\": {\"method\": \"text\", \"quantity\": 1, \"selector\": \"//*[contains(@class, \'re__pr-specs-content-item\')]/*[text()=\'Hướng nhà\']/following-sibling::*[1]\"}}', '{\"item\": \".js__product-link-for-product-id\", \"list\": \".js__card\"}');
INSERT INTO `resources` VALUES (2, 'muaban.net/bat-dong-san', 'https://muaban.net', 'ban-nha-dat-chung-cu', '?page=', 10, '{\"nk\": {\"regex\": \"Mã tin:\\\\s*(\\\\d+)\", \"method\": \"text\", \"quantity\": 1, \"selector\": \"//*[contains(@class, \'sc-6orc5o-15 jiDXp\')]//*[@class=\'date\']\"}, \"url\": {\"method\": \"url\"}, \"area\": {\"method\": \"text\", \"quantity\": 1, \"selector\": \"//*[(text()=\'Diện tích đất\')]/following-sibling::*[1]\"}, \"legal\": {\"method\": \"text\", \"quantity\": 1, \"selector\": \"//*[(text()=\'Giấy tờ pháp lý\')]/following-sibling::*[1]\"}, \"phone\": {\"method\": \"text\", \"quantity\": 1, \"selector\": \"//*[contains(@class, \'sc-lohvv8-15 fyGvhT\')]\"}, \"price\": {\"method\": \"text\", \"quantity\": 1, \"selector\": \"//*[contains(@class, \'sc-6orc5o-15 jiDXp\')]//*[@class=\'price\']\"}, \"floors\": {\"method\": \"text\", \"quantity\": 1, \"selector\": \"//*[(text()=\'Tổng số tầng\')]/following-sibling::*[1]\"}, \"images\": {\"method\": \"get_attribute\", \"quantity\": null, \"selector\": \"//*[contains(@class, \'sc-6orc5o-3 ljaVcC\')]//img\", \"attribute\": \"src\"}, \"address\": {\"method\": \"description\", \"selector\": \"//*[contains(@class, \'sc-6orc5o-15 jiDXp\')]/div[contains(@class, \'address\')]\"}, \"bedroom\": {\"method\": \"text\", \"quantity\": 1, \"selector\": \"//*[(text()=\'Số phòng ngủ\')]/following-sibling::*[1]\"}, \"subject\": {\"method\": \"text\", \"quantity\": 1, \"selector\": \"//*[contains(@class, \'sc-6orc5o-15 jiDXp\')]/h1\"}, \"bathroom\": {\"method\": \"text\", \"quantity\": 1, \"selector\": \"//*[(text()=\'Số phòng vệ sinh\')]/following-sibling::*[1]\"}, \"create_at\": {\"method\": \"time\"}, \"full_name\": {\"method\": \"text\", \"quantity\": 1, \"selector\": \"//span[contains(@class, \'title\')]\"}, \"description\": {\"method\": \"description\", \"selector\": \"//*[contains(@class, \'sc-6orc5o-18 gdAVnx\')]\"}, \"orientation\": {\"method\": \"text\", \"quantity\": 1, \"selector\": \"//*[(text()=\'Hướng cửa chính\')]/following-sibling::*[1]\"}}', '{\"item\": \"a.title\", \"list\": \".sc-q9qagu-4.iZrvBN\"}');
INSERT INTO `resources` VALUES (3, 'muaban.net/bat-dong-san', 'https://muaban.net', 'cho-thue-nha-dat', '?page=', 10, '{\"nk\": {\"regex\": \"Mã tin:\\\\s*(\\\\d+)\", \"method\": \"text\", \"quantity\": 1, \"selector\": \"//*[contains(@class, \'sc-6orc5o-15 jiDXp\')]//*[@class=\'date\']\"}, \"url\": {\"method\": \"url\"}, \"area\": {\"method\": \"text\", \"quantity\": 1, \"selector\": \"//*[(text()=\'Diện tích đất\')]/following-sibling::*[1]\"}, \"legal\": {\"method\": \"text\", \"quantity\": 1, \"selector\": \"//*[(text()=\'Giấy tờ pháp lý\')]/following-sibling::*[1]\"}, \"phone\": {\"method\": \"text\", \"quantity\": 1, \"selector\": \"//*[contains(@class, \'sc-lohvv8-15 fyGvhT\')]\"}, \"price\": {\"method\": \"text\", \"quantity\": 1, \"selector\": \"//*[contains(@class, \'sc-6orc5o-15 jiDXp\')]//*[@class=\'price\']\"}, \"floors\": {\"method\": \"text\", \"quantity\": 1, \"selector\": \"//*[(text()=\'Tổng số tầng\')]/following-sibling::*[1]\"}, \"images\": {\"method\": \"get_attribute\", \"quantity\": null, \"selector\": \"//*[contains(@class, \'sc-6orc5o-3 ljaVcC\')]//img\", \"attribute\": \"src\"}, \"address\": {\"method\": \"description\", \"selector\": \"//*[contains(@class, \'sc-6orc5o-15 jiDXp\')]/div[contains(@class, \'address\')]\"}, \"bedroom\": {\"method\": \"text\", \"quantity\": 1, \"selector\": \"//*[(text()=\'Số phòng ngủ\')]/following-sibling::*[1]\"}, \"subject\": {\"method\": \"text\", \"quantity\": 1, \"selector\": \"//*[contains(@class, \'sc-6orc5o-15 jiDXp\')]/h1\"}, \"bathroom\": {\"method\": \"text\", \"quantity\": 1, \"selector\": \"//*[(text()=\'Số phòng vệ sinh\')]/following-sibling::*[1]\"}, \"create_at\": {\"method\": \"time\"}, \"full_name\": {\"method\": \"text\", \"quantity\": 1, \"selector\": \"//span[contains(@class, \'title\')]\"}, \"description\": {\"method\": \"description\", \"selector\": \"//*[contains(@class, \'sc-6orc5o-18 gdAVnx\')]\"}, \"orientation\": {\"method\": \"text\", \"quantity\": 1, \"selector\": \"//*[(text()=\'Hướng cửa chính\')]/following-sibling::*[1]\"}}', '{\"item\": \"a.title\", \"list\": \".sc-q9qagu-4.iZrvBN\"}');

-- ----------------------------
-- Table structure for type_databases
-- ----------------------------
DROP TABLE IF EXISTS `type_databases`;
CREATE TABLE `type_databases`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `type_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of type_databases
-- ----------------------------
INSERT INTO `type_databases` VALUES (1, 'staging');
INSERT INTO `type_databases` VALUES (2, 'warehouse');

-- ----------------------------
-- Procedure structure for get_database_config
-- ----------------------------
DROP PROCEDURE IF EXISTS `get_database_config`;
delimiter ;;
CREATE PROCEDURE `get_database_config`(IN dbName varchar(200))
BEGIN
#     3.trả về toàn bộ thông tin của config_databases đó
    SELECT config_databases.*
#         1.Thực hiện liên kết bảng type_databases và config_databases
    FROM type_databases
             JOIN config_databases
                  ON type_databases.id = config_databases.type_database_id
#         2.thực hiện tìm kiếm loại database phù hợp với tham số truyền vào
    WHERE type_databases.type_name = dbName;
END
;;
delimiter ;

-- ----------------------------
-- Procedure structure for get_log_crawler
-- ----------------------------
DROP PROCEDURE IF EXISTS `get_log_crawler`;
delimiter ;;
CREATE PROCEDURE `get_log_crawler`()
BEGIN
#     1.1 tạo biến _id và _config_id để lưu lại log id và config id của log đó
    DECLARE _id INT DEFAULT 0;
    DECLARE _config_id INT DEFAULT 0;
#     1.2 thực hiện kiểm tra trong log có tồn tại ít nhất 1 dòng là FILE_PROCESSING
    IF !EXISTS(SELECT 'FILE_PROCESSING'
               FROM logs
               WHERE status = 'FILE_PROCESSING'
                 AND is_delete = 0
               LIMIT 1) THEN
        SELECT logs.id, logs.config_id
#         1.4.1 không thay đổi giá trị 2 biến
#        1.4.2 thực hiện việc gán giá trị log.id và log.config_id vào biến _id, _config_id
        INTO _id, _config_id
#         1.3 thực hiện join bảng logs và bảng config
        FROM logs
                 join configs on logs.config_id = configs.id
#         1.4 tìm kiếm 1 dòng log có status là FILE_PENDING hay FILE_ERROR chưa bị xóa của ngày hôm đó và của thông tin còn hoạt động
        WHERE (logs.status = 'FILE_PENDING' OR logs.status = 'FILE_ERROR')
          AND is_delete = 0
          AND DATE(logs.create_at) = CURRENT_DATE
          And configs.active = 1
        #     GROUP BY logs.id, logs.config_id
        ORDER BY CASE
                     WHEN logs.status = 'FILE_PENDING' THEN 1
                     WHEN logs.status = 'FILE_ERROR' THEN 2
                     END
        LIMIT 1;
#         1.5 Kiểm tra nếu config_id lấy được khác không(tức tìm được dòng có trạng thái hợp lệ)
        IF _config_id != 0 THEN
#             1.6 thiết lập trạng thái bị xóa cho dòng log đó
            UPDATE logs
            SET logs.is_delete = 1
            WHERE logs.id = _id;
            #               AND (logs.status = 'FILE_PENDING' OR logs.status = 'FILE_ERROR')
#               AND DATE(logs.create_at) = CURRENT_DATE;
# 1.7 thêm 1 dòng log mới có config_id, thời gian bắt đầu và thời giang tạo ngay lúc thêm và có trạng thái "FILE_PROCESSING"
            INSERT INTO logs (config_id, time_start, time_end, file_name, error_file_name, count_row, status,
                              create_at)
            VALUES (_config_id, NOW(), NULL, ' ', ' ', 0, 'FILE_PROCESSING', NOW());
        END IF;
#         1.8 Trả về các thông tin cần thiết cho việc crawl của _config_id lấy được
        SELECT configs.id,
               configs.email,
               configs.data_dir_path,
               configs.error_dir_path,
               configs.file_extension,
               configs.file_format,
               configs.prefix,
               configs.prefix_error,
               resources.scenario,
               resources.base_url,
               resources.limit_page,
               resources.paging_pattern,
               resources.source_page,
               resources.purpose,
               resources.navigate_scenario
        FROM resources
                 JOIN configs ON resources.id = configs.resource_id
                 JOIN logs ON logs.config_id = configs.id
        WHERE configs.id = _config_id
          AND logs.id = _id
          AND active = 1;
    END IF;
END
;;
delimiter ;

-- ----------------------------
-- Procedure structure for get_log_datamart
-- ----------------------------
DROP PROCEDURE IF EXISTS `get_log_datamart`;
delimiter ;;
CREATE PROCEDURE `get_log_datamart`()
BEGIN
#     1.1 tạo biến _id và _config_id để lưu lại log id và config id của log đó
    DECLARE _id INT DEFAULT 0;
DECLARE _config_id INT DEFAULT 0;
#     1.2 thực hiện kiểm tra trong log có tồn tại ít nhất 1 dòng là DATAMART_PROCESSING
IF !EXISTS(SELECT 'DATAMART_PROCESSING'
               FROM logs
               WHERE status = 'DATAMART_PROCESSING'
                 AND is_delete = 0
               LIMIT 1) THEN
SELECT logs.id, logs.config_id
#         1.4.1 không thay đổi giá trị 2 biến
#        1.4.2 thực hiện việc gán giá trị log.id và log.config_id vào biến _id, _config_id
INTO _id, _config_id
#         1.3 thực hiện join bảng logs và bảng config
FROM logs
         join configs on logs.config_id = configs.id
#         1.4 tìm kiếm 1 dòng log có status là DATAMART_PENDING hay DATAMART_ERROR chưa bị xóa của ngày hôm đó và của thông tin còn hoạt động
WHERE (logs.status = 'DATAMART_PENDING' OR logs.status = 'DATAMART_ERROR')
  AND is_delete = 0
  AND DATE(logs.create_at) = CURRENT_DATE
  And configs.active = 1
#     GROUP BY logs.id, logs.config_id
ORDER BY
    CASE
             WHEN logs.status = 'DATAMART_PENDING' THEN 1
             WHEN logs.status = 'DATAMART_ERROR' THEN 2
    END,
         logs.create_at ASC
LIMIT 1;
#         1.5 Kiểm tra nếu config_id lấy được khác không(tức tìm được dòng có trạng thái hợp lệ)
IF _config_id != 0 THEN
#             1.6 thiết lập trạng thái bị xóa cho dòng log đó
UPDATE logs
SET logs.is_delete = 1
WHERE logs.id = _id;
#               AND (logs.status = 'FILE_PENDING' OR logs.status = 'DATAMART_ERROR')
#               AND DATE(logs.create_at) = CURRENT_DATE;
# 1.7 thêm 1 dòng log mới có config_id, thời gian bắt đầu và thời giang tạo ngay lúc thêm và có trạng thái "DATAMART_PROCESSING"
INSERT INTO logs (config_id, time_start, time_end, file_name, error_file_name, count_row, status,
                  create_at)
VALUES (_config_id, NOW(), NULL, '', ' ', 0, 'DATAMART_PROCESSING', NOW());
END IF;
#         1.8 Trả về các thông tin cần thiết cho việc load của _config_id lấy được
SELECT configs.id,
       configs.email,
       configs.error_dir_path,
       configs.file_format,
       configs.prefix
FROM resources
         JOIN configs ON resources.id = configs.resource_id
         JOIN logs ON logs.config_id = configs.id

WHERE configs.id = _config_id
  AND logs.id = _id
  AND active = 1;
END IF;
END
;;
delimiter ;

-- ----------------------------
-- Procedure structure for get_log_staging
-- ----------------------------
DROP PROCEDURE IF EXISTS `get_log_staging`;
delimiter ;;
CREATE PROCEDURE `get_log_staging`()
BEGIN
#     1.1 tạo biến _id và _config_id để lưu lại log id và config id của log đó
    DECLARE _id INT DEFAULT 0;
DECLARE _config_id INT DEFAULT 0;
#     1.2 thực hiện kiểm tra trong log có tồn tại ít nhất 1 dòng là STAGING_PROCESSING
IF !EXISTS(SELECT 'STAGING_PROCESSING'
               FROM logs
               WHERE status = 'STAGING_PROCESSING'
                 AND is_delete = 0
               LIMIT 1) THEN
SELECT logs.id, logs.config_id
#         1.4.1 không thay đổi giá trị 2 biến
#        1.4.2 thực hiện việc gán giá trị log.id và log.config_id vào biến _id, _config_id
INTO _id, _config_id
#         1.3 thực hiện join bảng logs và bảng config
FROM logs
         join configs on logs.config_id = configs.id
#         1.4 tìm kiếm 1 dòng log có status là STAGING_PENDING hay STAGING_ERROR chưa bị xóa của ngày hôm đó và của thông tin còn hoạt động
WHERE (logs.status = 'STAGING_PENDING' OR logs.status = 'STAGING_ERROR')
  AND is_delete = 0
  AND DATE(logs.create_at) = CURRENT_DATE
  And configs.active = 1
#     GROUP BY logs.id, logs.config_id
ORDER BY
    CASE
             WHEN logs.status = 'STAGING_PENDING' THEN 1
             WHEN logs.status = 'STAGING_ERROR' THEN 2
    END,
         logs.create_at ASC
LIMIT 1;
#         1.5 Kiểm tra nếu config_id lấy được khác không(tức tìm được dòng có trạng thái hợp lệ)
IF _config_id != 0 THEN
#             1.6 thiết lập trạng thái bị xóa cho dòng log đó
UPDATE logs
SET logs.is_delete = 1
WHERE logs.id = _id;
#               AND (logs.status = 'FILE_PENDING' OR logs.status = 'STAGING_ERROR')
#               AND DATE(logs.create_at) = CURRENT_DATE;
# 1.7 thêm 1 dòng log mới có config_id, thời gian bắt đầu và thời giang tạo ngay lúc thêm và có trạng thái "STAGING_PROCESSING"
INSERT INTO logs (config_id, time_start, time_end, file_name, error_file_name, count_row, status,
                  create_at)
VALUES (_config_id, NOW(), NULL, '', ' ', 0, 'STAGING_PROCESSING', NOW());
END IF;
#         1.8 Trả về các thông tin cần thiết cho việc load của _config_id lấy được
SELECT configs.id,
       configs.email,
#        he dieu hanh khac thi sua
       CONCAT( configs.data_dir_path,'/',logs.file_name) as file_part,
       resources.name,
       configs.error_dir_path,
       configs.file_format,
       configs.prefix
FROM resources
         JOIN configs ON resources.id = configs.resource_id
         JOIN logs ON logs.config_id = configs.id

WHERE configs.id = _config_id
  AND logs.id = _id
  AND active = 1;
END IF;
END
;;
delimiter ;

-- ----------------------------
-- Procedure structure for get_log_transform
-- ----------------------------
DROP PROCEDURE IF EXISTS `get_log_transform`;
delimiter ;;
CREATE PROCEDURE `get_log_transform`()
BEGIN
    # 1.1 tạo biến _id và _config_id để lưu lại log id và config id của log đó
    DECLARE _id INT DEFAULT 0;
    DECLARE _config_id INT DEFAULT 0;
    # 1.2 thực hiện kiểm tra trong log có tồn tại ít nhất 1 dòng là TRANSFORM_PROCESSING
    IF !EXISTS(SELECT 'TRANSFORM_PROCESSING'
               FROM logs
               WHERE status = 'TRANSFORM_PROCESSING'
                 AND is_delete = 0
               LIMIT 1) THEN
        # Không tồn tại dòng nào có status là TRANSFORM_PROCESSING
        SELECT logs.id, logs.config_id
        # 1.4.1 không thay đổi giá trị 2 biến
        # 1.4.2 thực hiện việc gán giá trị log.id và log.config_id vào biến _id, _config_id
        INTO _id, _config_id
        # 1.3 thực hiện join bảng logs và bảng config
        FROM logs
                 join configs on logs.config_id = configs.id
        # 1.4 tìm kiếm 1 dòng log có status là TRANSFORM_PENDING hay TRANSFORM_ERROR chưa bị xóa của ngày hôm đó và của thông tin còn hoạt động
        WHERE (logs.status = 'TRANSFORM_PENDING' OR logs.status = 'TRANSFORM_ERROR')
          AND is_delete = 0
          AND DATE(logs.create_at) = CURRENT_DATE
          And configs.active = 1
        #  Sắp xếp ưu tiên dòng có status là TRANSFORM_PENDING trước
        ORDER BY CASE
                     WHEN logs.status = 'TRANSFORM_PENDING' THEN 1
                     WHEN logs.status = 'TRANSFORM_ERROR' THEN 2
                     END
        LIMIT 1;
        # 1.5 Kiểm tra nếu config_id lấy được khác không(tức tìm được dòng có trạng thái hợp lệ)
        IF _config_id != 0 THEN
            # 1.6 thiết lập trạng thái bị xóa cho dòng log đó
            UPDATE logs
            SET logs.is_delete = 1
            WHERE logs.id = _id;
            # 1.7 thêm 1 dòng log mới có config_id, thời gian bắt đầu và thời giang tạo ngay lúc thêm và có trạng thái "TRANSFORM_PROCESSING"
            INSERT INTO logs (config_id, time_start, time_end, file_name, error_file_name, count_row, status,
                              create_at)
            VALUES (_config_id, NOW(), NULL, ' ', ' ', 0, 'TRANSFORM_PROCESSING', NOW());
        END IF;
        # 1.8 Trả về các thông tin cần thiết cho việc crawl của _config_id lấy được
        SELECT configs.id,
               configs.error_dir_path,
               configs.file_format,
               configs.prefix,
               resources.name as source_name
        FROM resources
                 JOIN configs ON resources.id = configs.resource_id
                 JOIN logs ON logs.config_id = configs.id
        WHERE configs.id = _config_id
          AND logs.id = _id
          AND active = 1;
    END IF;
END
;;
delimiter ;

-- ----------------------------
-- Procedure structure for get_script_load_file_by_source
-- ----------------------------
DROP PROCEDURE IF EXISTS `get_script_load_file_by_source`;
delimiter ;;
CREATE PROCEDURE `get_script_load_file_by_source`(IN source ENUM ('muaban.net', 'batdongsan.com.vn'),
    IN file_path VARCHAR(255))
BEGIN
    DECLARE load_file_script TEXT;

    IF source = 'batdongsan.com.vn' THEN
        SET load_file_script = CONCAT(
                'truncate estate_daily_temp_batdongsan_com_vn;'
            , 'SET GLOBAL local_infile = TRUE;',
                'LOAD DATA LOCAL INFILE \'', file_path,
                '\' INTO TABLE estate_daily_temp_batdongsan_com_vn FIELDS TERMINATED BY \',\' OPTIONALLY ENCLOSED BY \'"\' LINES TERMINATED BY \'\\n\' IGNORE 1 LINES ',
                '(nk, url, area, email, legal, price, floors, images, address, bedroom, subject, bathroom, end_date, create_at, full_name, start_date, description, orientation);'
            , 'SET GLOBAL local_infile = FALSE;');
    ELSE
        SET load_file_script = CONCAT(
                'truncate estate_daily_temp_muaban_net;',
                'SET GLOBAL local_infile = TRUE;',
                'LOAD DATA LOCAL INFILE \'', file_path,
                '\' INTO TABLE estate_daily_temp_muaban_net FIELDS TERMINATED BY \',\' OPTIONALLY ENCLOSED BY \'"\' LINES TERMINATED BY \'\\n\' IGNORE 1 LINES ',
                '(nk, url, area, legal, phone, price, floors, images, address, bedroom, subject, bathroom, create_at, full_name, description, orientation);'
            , 'SET GLOBAL local_infile = FALSE;');
    END IF;
    SELECT load_file_script;
END
;;
delimiter ;

-- ----------------------------
-- Procedure structure for insert_log_crawler
-- ----------------------------
DROP PROCEDURE IF EXISTS `insert_log_crawler`;
delimiter ;;
CREATE PROCEDURE `insert_log_crawler`(_config_id INT,
                                    _file_name VARCHAR(200), _error_file_name VARCHAR(200), _count_row INT,
                                    _status VARCHAR(200))
BEGIN
    UPDATE logs
    SET time_end        = NOW(),
        file_name       = _file_name,
        error_file_name = _error_file_name,
        count_row       = _count_row,
        is_delete       = 1
    WHERE status = 'FILE_PROCESSING'
      AND config_id = _config_id;

    if _status = 'FILE_ERROR' THEN
        INSERT INTO logs (config_id, time_start, time_end, file_name, error_file_name, count_row, status,
                          create_at)
        VALUES (_config_id, NOW(), NULL, ' ', ' ', 0, _status, NOW());
    ELSEIF _status = 'STAGING_PENDING' THEN
        INSERT INTO logs (config_id, time_start, time_end, file_name, error_file_name, count_row, status,
                          create_at)
        VALUES (_config_id, NOW(), NULL, ' ', ' ', 0, _status, NOW());
    END IF;
END
;;
delimiter ;

-- ----------------------------
-- Procedure structure for insert_log_staging
-- ----------------------------
DROP PROCEDURE IF EXISTS `insert_log_staging`;
delimiter ;;
CREATE PROCEDURE `insert_log_staging`(_config_id INT,
                                    _file_name VARCHAR(200), _error_file_name VARCHAR(200), _count_row INT,
                                    _status VARCHAR(200))
BEGIN
    UPDATE logs
    SET time_end        = NOW(),
        file_name       = _file_name,
        error_file_name = _error_file_name,
        count_row       = _count_row,
        is_delete       = 1
    WHERE status = 'STAGING_PROCESSING'
      AND config_id = _config_id;

    if _status = 'STAGING_ERROR' THEN
        INSERT INTO logs (config_id, time_start, time_end, file_name, error_file_name, count_row, status,
                          create_at)
        VALUES (_config_id, NOW(), NULL, ' ', ' ', 0, _status, NOW());
    ELSEIF _status = 'WAREHOUSE_PENDING' THEN
        INSERT INTO logs (config_id, time_start, time_end, file_name, error_file_name, count_row, status,
                          create_at)
        VALUES (_config_id, NOW(), NULL, ' ', ' ', 0, _status, NOW());
    END IF;
END
;;
delimiter ;

-- ----------------------------
-- Procedure structure for insert_log_transform
-- ----------------------------
DROP PROCEDURE IF EXISTS `insert_log_transform`;
delimiter ;;
CREATE PROCEDURE `insert_log_transform`(_config_id INT,
                                      _count_row INT,
                                      _error_file_name VARCHAR(200),
                                      _status VARCHAR(200))
BEGIN
    UPDATE logs
    SET time_end        = NOW(),
        file_name       = NULL,
        error_file_name = _error_file_name,
        count_row       = _count_row,
        is_delete       = 1
    WHERE status = 'TRANSFORM_PROCESSING'
      AND config_id = _config_id;

    if _status = 'TRANSFORM_ERROR' THEN
        INSERT INTO logs (config_id, time_start, time_end, file_name, error_file_name, count_row, status,
                          create_at)
        VALUES (_config_id, NOW(), NULL, ' ', _error_file_name, 0, _status, NOW());
    ELSEIF _status = 'TRANSFORM_PENDING' THEN
        INSERT INTO logs (config_id, time_start, time_end, file_name, error_file_name, count_row, status,
                          create_at)
        VALUES (_config_id, NOW(), NULL, ' ', ' ', _count_row, _status, NOW());
    END IF;
END
;;
delimiter ;

-- ----------------------------
-- Procedure structure for insert_new_log_crawler
-- ----------------------------
DROP PROCEDURE IF EXISTS `insert_new_log_crawler`;
delimiter ;;
CREATE PROCEDURE `insert_new_log_crawler`()
BEGIN
    INSERT INTO logs (config_id, time_start, time_end, file_name, error_file_name, count_row, status, create_at)
    VALUES (1, NOW(), NULL, ' ', ' ', 0, 'FILE_PENDING', NOW()),
           (2, NOW(), NULL, ' ', ' ', 0, 'FILE_PENDING', NOW());
END
;;
delimiter ;

SET FOREIGN_KEY_CHECKS = 1;
