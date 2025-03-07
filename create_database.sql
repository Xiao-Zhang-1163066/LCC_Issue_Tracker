CREATE DATABASE lccapp;
USE lccapp;
CREATE TABLE `users` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(20) NOT NULL,
  `password_hash` char(60) BINARY NOT NULL COMMENT 'Bcrypt Password Hash and Salt (60 bytes)',
  `email` varchar(320) NOT NULL COMMENT 'Maximum email address length according to RFC5321 section 4.5.3.1 is 320 characters (64 for local-part, 1 for at sign, 255 for domain)',
  `first_name` varchar(50) NOT NULL,
  `last_name` varchar(50) NOT NULL,
  `location` varchar(50) NOT NULL,
  `profile_image` varchar(255),
  `role` enum('visitor','helper','admin') NOT NULL DEFAULT 'visitor',
  `status` enum('active','inactive') NOT NULL DEFAULT 'active',
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `username` (`username`)
);

CREATE TABLE `issues` (
  `issue_id` INT NOT NULL AUTO_INCREMENT,
  `user_id` INT NOT NULL,
  `summary` VARCHAR(255) NOT NULL COMMENT 'Short title of the issue',
  `description` TEXT COMMENT 'Detailed explanation of the issue',
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'Timestamp when the issue was created',
  `issue_status` ENUM('new', 'open', 'stalled', 'resolved') NOT NULL DEFAULT 'new' COMMENT 'Current status of the issue',
  PRIMARY KEY (`issue_id`),
  FOREIGN KEY (`user_id`) REFERENCES `users`(`user_id`) ON DELETE CASCADE
);

CREATE TABLE `comments` (
  `comment_id` INT NOT NULL AUTO_INCREMENT,
  `issue_id` INT NOT NULL,
  `user_id` INT NOT NULL,
  `content` TEXT NOT NULL COMMENT 'Content of the comment',
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'Timestamp when the comment was created',
  PRIMARY KEY (`comment_id`),
  FOREIGN KEY (`issue_id`) REFERENCES `issues`(`issue_id`) ON DELETE CASCADE,
  FOREIGN KEY (`user_id`) REFERENCES `users`(`user_id`) ON DELETE CASCADE
);
