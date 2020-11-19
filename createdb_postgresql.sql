drop table if exists addresses;
drop table if exists categories;

create table categories(
    id serial primary key,
    user_id integer,
    name varchar(255),
    created timestamp
);

create table addresses(
    id serial primary key,
    user_id integer,
    address varchar(500),
    link_to_ya_map text,
    created timestamp,
    category_id integer REFERENCES categories(id),
    is_shown integer default 1 not null
);


insert into categories (id, name, user_id)
values
    (1, 'Рабочий', 266431296),
    (2, 'Домашний', 266431296),
    (3, 'Другой', 266431296);

insert into addresses (id, address, link_to_ya_map, created, user_id, category_id)
values
    (1, 'Домашний адрес 1', 'link1', now(), 266431296, 2),
    (2, 'Рабочий адрес 1', 'link2', now(), 266431296, 1),
    (3, 'Домашний адрес 2', 'link3', now(), 266431296, 2),
    (4, 'Домашний адрес 3', 'link4', now(), 266431296, 2);
