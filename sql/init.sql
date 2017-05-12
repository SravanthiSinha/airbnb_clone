/*script to have following change - MySQL instance will contain 2 databases, 2 new users with different privileges*/

/* create users */
CREATE USER 'airbnb_user_dev'@'%' IDENTIFIED BY 'user_dev';
CREATE USER 'airbnb_user_prod'@'localhost' IDENTIFIED BY 'user_prod';

/* create databases */
CREATE DATABASE airbnb_dev CHARACTER SET utf8 COLLATE utf8_general_ci;
CREATE DATABASE airbnb_prod CHARACTER SET utf8 COLLATE utf8_general_ci;

/*grant privallages */
GRANT ALL PRIVILEGES ON airbnb_dev.* TO 'airbnb_user_dev'@'%';
GRANT ALL PRIVILEGES ON airbnb_prod.* TO 'airbnb_user_prod'@'localhost';
FLUSH PRIVILEGES;
