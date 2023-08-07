DROP TABLE IF EXISTS usuario;
DROP TABLE IF EXISTS questoes;

CREATE TABLE IF NOT EXISTS usuario (
    id INT PRIMARY KEY AUTO_INCREMENT,
    password VARCHAR(150) NOT NULL,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    turma VARCHAR(50) DEFAULT 'default',
    privilegio VARCHAR(50) DEFAULT 'usuario'
);

CREATE TABLE questoes (
    id INT PRIMARY KEY AUTO_INCREMENT,
    colecao VARCHAR(50) NOT NULL,
    titulo VARCHAR(50) NOT NULL,
    texto VARCHAR(244) NOT NULL,
    imgPath VARCHAR(50) DEFAULT NULL,
    respostaCorreta VARCHAR(50) NOT NULL,
    alternativa1 VARCHAR(50),
    alternativa2 VARCHAR(50),
    alternativa3 VARCHAR(50),
    alternativa4 VARCHAR(50)
);

INSERT INTO `arduck`.`usuario` (`id`, `password`, `nome`, `email`, `turma`, `privilegio`) VALUES ('1', 'otavio1234', 'Otavio Zordan', 'otavio.com', 'defult', 'administrador');
