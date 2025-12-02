USE legacy_corp;

CREATE TABLE products (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255),
    description TEXT
);

CREATE TABLE secrets (
    id INT PRIMARY KEY AUTO_INCREMENT,
    key_name VARCHAR(255),
    secret_value VARCHAR(255)
);

INSERT INTO products (name, description) VALUES
('Clavier Modèle A', 'Un clavier standard.'),
('Souris Optique', 'Une souris précise et ergonomique.');

INSERT INTO secrets (key_name, secret_value) VALUES
('api_key_prototype', 'Securinets{Err0rs_L34k_M0r3_Th4n_W4t3r}');