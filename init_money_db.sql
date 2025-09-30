CREATE DATABASE IF NOT EXISTS money_vision_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE money_vision_db;

CREATE TABLE IF NOT EXISTS users (
  user_id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS financial_records (
  record_id BIGINT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  year INT NOT NULL,
  month TINYINT NOT NULL,
  amount DECIMAL(12,2) NOT NULL,
  CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
  UNIQUE KEY ux_user_year_month (user_id, year, month)
);

INSERT INTO users (name) VALUES ('JaneDoe') ON DUPLICATE KEY UPDATE name=name;

