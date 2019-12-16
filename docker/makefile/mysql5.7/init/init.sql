-- 在mysql数据库中创建指定的用户，并设置其的登陆密码

CREATE USER z1987_user@localhost IDENTIFIED BY 'z1987_pw';
CREATE USER z1987_user@'%' IDENTIFIED BY 'z1987_pw';

-- 创建指定的库并赋予权限

-- Create database: z1987_admin

CREATE DATABASE `z1987_admin` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci */;

grant all privileges on z1987_admin.* to z1987_user@localhost;
grant all privileges on z1987_admin.* to z1987_user@'%';
