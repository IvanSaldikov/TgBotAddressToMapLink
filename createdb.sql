drop table if exists addresses;
drop table if exists categories;

create table addresses(
    id integer primary key,
    user_id integer,
    address varchar(500),
    link_to_ya_map text,
    created datetime,
    category_id integer,
    is_shown integer default 1 not null,
    FOREIGN KEY(category_id) REFERENCES categories(id)
);

create table categories(
    id integer primary key,
    user_id integer,
    name varchar(255),
    created datetime
);

insert into categories (id, name, user_id)
values
    (1, "Рабочий", 266431296),
    (2, "Домашний", 266431296),
    (3, "Другой", 266431296);

insert into addresses (id, address, link_to_ya_map, created, user_id, category_id)
values
    (1, "Домашний адрес 1", "link1", date('now', 'localtime'), 266431296, 2),
    (2, "Рабочий адрес 1", "link2", date('now', 'localtime'), 266431296, 1),
    (3, "Домашний адрес 2", "link3", date('now', 'localtime'), 266431296, 2),
    (4, "Домашний адрес 3", "link4", date('now', 'localtime'), 266431296, 2);
