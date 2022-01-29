-- CREATE DATABASE IF NOT EXISTS book_store;

DROP TABLE IF EXISTS carte_la_stoc;
DROP TABLE IF EXISTS carte_la_autor;
DROP TABLE IF EXISTS carte;
DROP TABLE IF EXISTS autor;


CREATE TABLE IF NOT EXISTS carte (
	id_carte INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
	isbn CHAR(13) NOT NULL , 
	titlu VARCHAR(50) NOT NULL,
	editura VARCHAR(20) NOT NULL,
	an_publicare INT NOT NULL,
	gen_literar VARCHAR(30) NOT NULL,
	
    UNIQUE KEY unique_ISBN (isbn),
    UNIQUE KEY unique_Titlu (titlu)
);

CREATE INDEX idx_an_publicare ON carte(an_publicare); 
CREATE INDEX idx_gen_literar ON carte(gen_literar); 


CREATE TABLE IF NOT EXISTS carte_la_stoc(
	id_stoc INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
	id_carte INT NOT NULL,
	stoc INT NOT NULL,
	pret FLOAT NOT NULL,
	
	FOREIGN KEY (id_carte) 
        REFERENCES carte(id_carte)
);

CREATE TABLE IF NOT EXISTS autor (
	id_autor INT PRIMARY KEY AUTO_INCREMENT, 
	prenume VARCHAR(20) NOT NULL,
	nume VARCHAR(20) NOT NULL
);

CREATE INDEX idx_prenume ON autor(prenume); 
CREATE INDEX idx_nume ON autor(nume); 

CREATE TABLE IF NOT EXISTS carte_la_autor (
	id_carte INT NOT NULL, 
	id_autor INT NOT NULL,
	autor_index INT NOT NULL,

	PRIMARY KEY (id_carte, id_autor),

	FOREIGN KEY (id_carte) 
        REFERENCES carte(id_carte),

	FOREIGN KEY (id_autor) 
        REFERENCES autor(id_autor)
);

COMMIT;
