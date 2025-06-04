SELECT * FROM create_estudante('Vicente José', '1237');
SELECT * FROM create_estudante('Yannick Matimbe', '6108');
SELECT * FROM create_estudante('João Mateus', '1238');
SELECT * FROM create_estudante('Sérgio Cunha', '1239');
SELECT * FROM update_estudante(7, 'Yannick Matimbe', '6109', 0);
SELECT * FROM update_estudante(7, 'Yannick Rafael', '6109', 3);
SELECT * FROM delete_estudante(8);


SELECT * FROM create_curso('Licenciatura em Contabilidade e Auditoria', 'LCA', 1);
SELECT * FROM create_curso('Licenciatura em Engenharia e Ciência dos Computadores', '(LECC)', 1);
SELECT * FROM create_curso('Licenciatura em Engenharia Electromecânica (', '(LEMEC)', 1);
SELECT * FROM update_curso(3, NULL,'LECC', 2);
SELECT * FROM update_curso(4, 'Licenciatura em Engenharia Electromecânica',NULL, 2);
SELECT * FROM update_curso(4, NULL, 'LEMEC', 2);
SELECT * FROM delete_curso(2);
SELECT * FROM create_curso('Licenciatura em Engenharia e Ciência dos Computadores', 'LECC', 1);


SELECT * FROM create_cadeira('Redes de Computadores', 'RED-COMP', 3, 'https://link.com', 1);
SELECT * FROM create_cadeira('Sistemas Hidráulicos ', 'SIS-HID', 4, 'https://link.com');
SELECT * FROM update_cadeira(2, 'Sistema Hidráulico', NULL, NULL, NULL, 2);
SELECT * FROM update_cadeira(2, NULL, 'SISHID', NULL, NULL, 2);
SELECT * FROM update_cadeira(2, NULL, NULL, NULL, 'novo link', NULL);
SELECT * FROM delete_cadeira(2, 3);
SELECT * FROM delete_cadeira(1);
SELECT * FROM create_cadeira('Cadeira 1', 'C1', 3, 'https://link1.com');
SELECT * FROM create_cadeira('Cadeira 2', 'C2', 3, 'https://link2.com');
SELECT * FROM create_cadeira('Cadeira 3', 'C3', 3, 'https://link3.com');
SELECT * FROM create_cadeira('Cadeira 4', 'C4', 3, 'https://link4.com');
SELECT * FROM create_cadeira('Cadeira 5', 'C5', 3, 'https://link5.com');


SELECT * FROM create_avaliacao('Teste 1', 'T1', 3, 200);
SELECT * FROM create_avaliacao('Teste 2', 'T2', 3, 200);
SELECT * FROM create_avaliacao('Mini-Teste 1', 'MT1', 3, 100);
SELECT * FROM create_avaliacao('Mini-Teste 2', 'MT2', 3, 100);
SELECT * FROM create_avaliacao('Mini-Teste 3', 'MT3', 3, 100);
SELECT * FROM create_avaliacao('Mini-Teste 4', 'MT4', 3, 100);
SELECT * FROM create_avaliacao('Test For Test', 'TFT', 4, 30);
SELECT * FROM update_avaliacao(7, 'Tested', NULL, NULL, NULL);
SELECT * FROM update_avaliacao(7, NULL, 'TT', NULL, NULL);
SELECT * FROM delete_avaliacao(7);


SELECT * FROM create_performance(45, 7, 3);
SELECT * FROM create_performance(68, 6, 3);
SELECT * FROM create_performance(90, 9, 3);
SELECT * FROM update_performance(1, 110);
SELECT * FROM delete_performance(1);