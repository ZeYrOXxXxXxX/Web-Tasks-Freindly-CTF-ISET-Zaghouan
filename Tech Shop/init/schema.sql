CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    description VARCHAR(255),
    price DECIMAL(10,2)
);

INSERT INTO products (name, description, price) VALUES 
('Gaming Laptop', 'Runs everything ultra', 1500.00),
('Mechanical Keyboard', 'Clicky clack', 100.00),
('USB Rubber Ducky', 'For educational purposes only', 49.99),
('CTF Guide', 'How to hack (legally)', 29.99);

-- Grant FILE privilege for INTO OUTFILE
GRANT FILE ON *.* TO 'ctf_player'@'%';
FLUSH PRIVILEGES;
