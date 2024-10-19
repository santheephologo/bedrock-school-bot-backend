-- Create table for 'bots'
CREATE TABLE `bots` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `name` VARCHAR(255) NOT NULL UNIQUE,
  `agent_id` VARCHAR(255) NOT NULL,
  `alias_id` VARCHAR(255) NOT NULL,
  `is_active` BOOLEAN DEFAULT TRUE,
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Create table for 'clients'
CREATE TABLE `clients` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `username` VARCHAR(50) NOT NULL UNIQUE,
  `email` VARCHAR(120) NOT NULL,
  `password` VARCHAR(128) NOT NULL,
  `first_name` VARCHAR(50),
  `last_name` VARCHAR(50),
  `is_active` BOOLEAN DEFAULT TRUE,
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Create table for 'client_bots'
CREATE TABLE `client_bots` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `client_id` INT NOT NULL,
  `bot_id` INT NOT NULL,
  `name` VARCHAR(100) NOT NULL,
  `tkns_remaining` INT DEFAULT 0,
  `tkns_used` INT DEFAULT 0,
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (`client_id`) REFERENCES `clients`(`id`) ON DELETE CASCADE,
  FOREIGN KEY (`bot_id`) REFERENCES `bots`(`id`) ON DELETE CASCADE
);

-- Create table for 'chat_histories'
CREATE TABLE `chat_histories` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `session_id` VARCHAR(255) NOT NULL UNIQUE,
  `messages` JSON NOT NULL DEFAULT (JSON_ARRAY()),
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Create table for 'hologo'
CREATE TABLE `hologo` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `username` VARCHAR(50) NOT NULL UNIQUE,
  `tkns_remaining` INT DEFAULT 0,
  `tkn_used` INT DEFAULT 0,
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP
);
