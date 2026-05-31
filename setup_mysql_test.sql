-- Prepares a MySQL server for AirBnB clone test environment
-- Creates database hbnb_test_db, user hbnb_test with required privileges

-- Create the test database if it doesn't exist
CREATE DATABASE IF NOT EXISTS hbnb_test_db;

-- Create the test user if not exists
CREATE USER IF NOT EXISTS 'hbnb_test'@'localhost' IDENTIFIED BY 'hbnb_test_pwd';

-- Grant all privileges on hbnb_test_db to hbnb_test
GRANT ALL PRIVILEGES ON hbnb_test_db.* TO 'hbnb_test'@'localhost';

-- Grant SELECT privilege on performance_schema to hbnb_test
GRANT SELECT ON performance_schema.* TO 'hbnb_test'@'localhost';

-- Apply privilege changes
FLUSH PRIVILEGES;
