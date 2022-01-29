DROP TABLE IF EXISTS jwt_blacklist;

DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS user_role;

CREATE TABLE IF NOT EXISTS user_role(
    id_role INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    role_name VARCHAR(10) NOT NULL    
);

CREATE TABLE IF NOT EXISTS user (
	id_user INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
	email VARCHAR(50) NOT NULL, 
    user_password VARCHAR(100) NOT NULL, 

    id_role INT NOT NULL,
	
    UNIQUE KEY unique_email (email),

    FOREIGN KEY (id_role) 
        REFERENCES user_role(id_role)
);


CREATE TABLE IF NOT EXISTS jwt_blacklist (
	id_bjwt INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
	blacklisted_jwt VARCHAR(500) NOT NULL
);

INSERT INTO user_role (role_name) VALUES ("client");
INSERT INTO user_role (role_name) VALUES ("admin");
