drop table if exists users;
CREATE TABLE users(
    id BIGINT GENERATED ALWAYS AS IDENTITY,
    PRIMARY KEY(id),
    hash_firstname TEXT NOT NULL,
    hash_lastname TEXT NOT NULL,
    purchase_date date,
    gender VARCHAR(6) NOT NULL CHECK (gender IN ('male', 'female'))
);

INSERT INTO users(hash_firstname, hash_lastname, purchase_date, gender)
SELECT md5(RANDOM()::TEXT), md5(RANDOM()::TEXT), generate_series(timestamp '2022-01-01', '2022-01-10', '1 day')::date , CASE WHEN RANDOM() < 0.5 THEN 'male' ELSE 'female' END FROM generate_series(1, 1000000);