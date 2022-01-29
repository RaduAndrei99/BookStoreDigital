INSERT INTO carte (isbn, titlu, editura, an_publicare, gen_literar) VALUES ("9789734648887", "Sapiens. Scurta istorie a omenirii", "Polirom", 2017, "Stiinte umaniste");
INSERT INTO carte (isbn, titlu, editura, an_publicare, gen_literar) VALUES ("9789734671991", "Homo deus. Scurta istorie a viitorului", "Polirom", 2018, "Stiinte umaniste");
INSERT INTO carte (isbn, titlu, editura, an_publicare, gen_literar) VALUES ("9786066096133", "Hotul de carti", "Rao", 2011, "Fictiune");
INSERT INTO carte (isbn, titlu, editura, an_publicare, gen_literar) VALUES ("9786060065647", "Crima si pedeapsa", "Rao", 2021, "Fictiune");
INSERT INTO carte (isbn, titlu, editura, an_publicare, gen_literar) VALUES ("9786063332586", "Curajul de a nu fi pe placul celorlalti", "Litera", 2021, "Dezvoltare personala");
INSERT INTO carte (isbn, titlu, editura, an_publicare, gen_literar) VALUES ("9786063366796", "Pamantul fagaduintei", "Litera", 2020, "Memorii si jurnale");
INSERT INTO carte (isbn, titlu, editura, an_publicare, gen_literar) VALUES ("9786063330087", "Povestea mea", "Litera", 2018, "Memorii si jurnale");
INSERT INTO carte (isbn, titlu, editura, an_publicare, gen_literar) VALUES ("9786069748534", "Despre sensul vietii", "Bookzone", 2021, "Stiinte umaniste");

INSERT INTO autor (prenume, nume) VALUES ("Yuval Noah", "Harari");
INSERT INTO autor (prenume, nume) VALUES ("Markus", "Zusak");
INSERT INTO autor (prenume, nume) VALUES ("Fiodor Mihailovici", "Dostoievski");
INSERT INTO autor (prenume, nume) VALUES ("Kishimi", "Ichiro");
INSERT INTO autor (prenume, nume) VALUES ("Koga", "Fumitake");
INSERT INTO autor (prenume, nume) VALUES ("Barack", "Obama");
INSERT INTO autor (prenume, nume) VALUES ("Michelle", "Obama");
INSERT INTO autor (prenume, nume) VALUES ("Mihai", "Morar");
INSERT INTO autor (prenume, nume) VALUES ("Constantin", "Necula");

INSERT INTO carte_la_stoc(id_carte, stoc, pret) VALUES ((SELECT id_carte FROM carte WHERE isbn = "9789734648887"), 51, 55.2);
INSERT INTO carte_la_stoc(id_carte, stoc, pret) VALUES ((SELECT id_carte FROM carte WHERE isbn = "9789734671991"), 55, 60.5);
INSERT INTO carte_la_stoc(id_carte, stoc, pret) VALUES ((SELECT id_carte FROM carte WHERE isbn = "9786066096133"), 15, 78.1);
INSERT INTO carte_la_stoc(id_carte, stoc, pret) VALUES ((SELECT id_carte FROM carte WHERE isbn = "9786060065647"), 25, 89);
INSERT INTO carte_la_stoc(id_carte, stoc, pret) VALUES ((SELECT id_carte FROM carte WHERE isbn = "9786063332586"), 21, 56);
INSERT INTO carte_la_stoc(id_carte, stoc, pret) VALUES ((SELECT id_carte FROM carte WHERE isbn = "9786069748534"), 100, 45);

INSERT INTO carte_la_autor(id_carte, id_autor, autor_index) VALUES ((SELECT id_carte from CARTE where isbn="9789734648887"), 
(SELECT id_autor FROM autor WHERE nume="Harari" AND prenume="Yuval Noah"), 1);

INSERT INTO carte_la_autor(id_carte, id_autor, autor_index) VALUES ((SELECT id_carte from CARTE where isbn="9789734671991"), 
(SELECT id_autor FROM autor WHERE nume="Harari" AND prenume="Yuval Noah"), 1);

INSERT INTO carte_la_autor(id_carte, id_autor, autor_index) VALUES ((SELECT id_carte from CARTE where isbn="9786066096133"), 
(SELECT id_autor FROM autor WHERE nume="Zusak" AND prenume="Markus"), 2);

INSERT INTO carte_la_autor(id_carte, id_autor, autor_index) VALUES ((SELECT id_carte from CARTE where isbn="9786060065647"), 
(SELECT id_autor FROM autor WHERE nume="Dostoievski" AND prenume="Fiodor Mihailovici"), 3);

INSERT INTO carte_la_autor(id_carte, id_autor, autor_index) VALUES ((SELECT id_carte from CARTE where isbn="9786063332586"), 
(SELECT id_autor FROM autor WHERE nume="Ichiro" AND prenume="Kishimi"), 4);

INSERT INTO carte_la_autor(id_carte, id_autor, autor_index) VALUES ((SELECT id_carte from CARTE where isbn="9786063332586"), 
(SELECT id_autor FROM autor WHERE nume="Fumitake" AND prenume="Koga"), 5);

INSERT INTO carte_la_autor(id_carte, id_autor, autor_index) VALUES ((SELECT id_carte from CARTE where isbn="9786063366796"), 
(SELECT id_autor FROM autor WHERE nume="Obama" AND prenume="Barack"), 6);

INSERT INTO carte_la_autor(id_carte, id_autor, autor_index) VALUES ((SELECT id_carte from CARTE where isbn="9786063330087"), 
(SELECT id_autor FROM autor WHERE nume="Obama" AND prenume="Michelle"), 7);

INSERT INTO carte_la_autor(id_carte, id_autor, autor_index) VALUES ((SELECT id_carte from CARTE where isbn="9786069748534"), 
(SELECT id_autor FROM autor WHERE nume="Morar" AND prenume="Mihai"), 8);

INSERT INTO carte_la_autor(id_carte, id_autor, autor_index) VALUES ((SELECT id_carte from CARTE where isbn="9786069748534"), 
(SELECT id_autor FROM autor WHERE nume="Necula" AND prenume="Constantin"), 9);
commit;