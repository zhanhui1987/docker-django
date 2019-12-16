-- Create database: z1987_admin

CREATE DATABASE `z1987_admin` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci */;

grant all privileges on z1987_admin.* to z1987_user@localhost;
grant all privileges on z1987_admin.* to z1987_user@'%';
