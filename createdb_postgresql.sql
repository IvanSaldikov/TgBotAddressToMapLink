drop table if exists addresses;
drop table if exists categories;
drop sequence if exists addr_id_seq;
drop sequence if exists cat_id_seq;

CREATE SEQUENCE cat_id_seq;
CREATE SEQUENCE addr_id_seq;

create table categories(
    id int NOT NULL DEFAULT nextval('cat_id_seq') PRIMARY KEY,
    user_id integer,
    name varchar(255),
    created timestamp
);
create table addresses(
    id int NOT NULL DEFAULT nextval('addr_id_seq') PRIMARY KEY,
    user_id integer,
    address varchar(500),
    link_to_ya_map text,
    created timestamp,
    category_id integer,
    is_shown integer default 1 not null,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET DEFAULT
);

ALTER SEQUENCE cat_id_seq OWNED BY categories.id;
ALTER SEQUENCE addr_id_seq OWNED BY addresses.id;


insert into categories (name, user_id)
values
    ('Рабочий', 266431296),
    ('Домашний', 266431296),
    ('Другой', 266431296);

insert into addresses (address, link_to_ya_map, created, user_id, category_id)
values
    ('Домашний адрес 1', 'link1', now(), 266431296, 2),
    ('Рабочий адрес 1', 'link2', now(), 266431296, 1),
    ('Домашний адрес 2', 'link3', now(), 266431296, 2),
    ('Домашний адрес 3', 'link4', now(), 266431296, 2);
