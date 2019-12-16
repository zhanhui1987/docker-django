-- 在mysql数据库中创建指定的用户，并设置其的登陆密码

CREATE USER z1987_user@localhost IDENTIFIED BY 'z1987_pw';
CREATE USER z1987_user@'%' IDENTIFIED BY 'z1987_pw';
