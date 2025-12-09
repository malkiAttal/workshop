
CREATE TABLE IF NOT EXISTS items (
    id SERIAL PRIMARY KEY,
    name TEXT,
    price NUMERIC
);
INSERT INTO items (name, price) VALUES ('apple',1.5),('banana',2.0);
