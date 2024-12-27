-- Create table for 'bots'
CREATE TABLE
  `bots` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(255) NOT NULL UNIQUE,
    `assistant_id` VARCHAR(255) NOT NULL,
    `is_active` BOOLEAN DEFAULT TRUE,
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP
  );

-- Create table for 'clients'
CREATE TABLE
  `clients` (
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
CREATE TABLE
  `client_bots` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `client_id` INT NOT NULL,
    `bot_id` INT NOT NULL,
    `name` VARCHAR(100) NOT NULL,
    `tkns_remaining` INT DEFAULT 0,
    `tkns_used` INT DEFAULT 0,
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (`client_id`) REFERENCES `clients` (`id`) ON DELETE CASCADE,
    FOREIGN KEY (`bot_id`) REFERENCES `bots` (`id`) ON DELETE CASCADE
  );

-- Create table for 'chat_histories'
CREATE TABLE
  `chat_histories` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `session_id` VARCHAR(255) NOT NULL UNIQUE,
    `thread_id` VARCHAR(255) NOT NULL UNIQUE,
    `messages` JSON NOT NULL DEFAULT (JSON_ARRAY ()),
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP
  );

-- Create table for 'hologo'
CREATE TABLE
  `hologo` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `username` VARCHAR(50) NOT NULL UNIQUE,
    `tkns_remaining` INT DEFAULT 0,
    `tkn_used` INT DEFAULT 0,
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP
  );

INSERT INTO
  `bots` (`name`, `assistant_id`, `is_active`)
VALUES
  ('HospitalityBot', 'AST123456', TRUE),
  ('EducationBot', 'AST789012', TRUE),
  ('FitnessBot', 'AST345678', FALSE);

INSERT INTO
  `clients` (
    `username`,
    `email`,
    `password`,
    `first_name`,
    `last_name`,
    `is_active`
  )
VALUES
  (
    'john_doe',
    'john.doe@example.com',
    'hashedpassword123',
    'John',
    'Doe',
    TRUE
  ),
  (
    'jane_smith',
    'jane.smith@example.com',
    'hashedpassword456',
    'Jane',
    'Smith',
    TRUE
  ),
  (
    'alice_jones',
    'alice.jones@example.com',
    'hashedpassword789',
    'Alice',
    'Jones',
    FALSE
  );

INSERT INTO
  `client_bots` (
    `client_id`,
    `bot_id`,
    `name`,
    `tkns_remaining`,
    `tkns_used`
  )
VALUES
  (1, 1, 'Primary Science - Stage 3', 100, 50),
  (2, 2, 'Education Guide', 200, 30),
  (3, 3, 'Workout Partner', 0, 100);

INSERT INTO
  `chat_histories` (`session_id`, `thread_id`, `messages`)
VALUES
  (
    'sess001',
    'thread001',
    '[{"user": "Hi!", "bot": "Hello! How can I help you today?"}]'
  ),
  (
    'sess002',
    'thread002',
    '[{"user": "Tell me about your services.", "bot": "Sure! Here are our services..."}]'
  ),
  (
    'sess003',
    'thread003',
    '[{"user": "I need help with booking.", "bot": "Let me guide you through the process."}]'
  );

INSERT INTO
  `hologo` (`username`, `tkns_remaining`, `tkn_used`)
VALUES
  ('john_hologo', 300, 150),
  ('jane_hologo', 100, 200),
  ('alice_hologo', 50, 250);