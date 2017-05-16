/*script to have following change - MySQL instance will contain a new test datbase and new  test user with all privileges*/

/* create user */
CREATE USER 'airbnb_user_test'@'%' IDENTIFIED BY 'user_test';

/* create database */
CREATE DATABASE airbnb_test CHARACTER SET utf8 COLLATE utf8_general_ci;

/*grant privallages */
GRANT ALL PRIVILEGES ON airbnb_test.* TO 'airbnb_user_test'@'%';

FLUSH PRIVILEGES;
