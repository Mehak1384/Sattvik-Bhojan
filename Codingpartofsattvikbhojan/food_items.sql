create table if not exists food_items (
    id serial primary key,
    name varchar(100) not null,
    category varchar(50),
    price decimal(10,2) not null,
    available boolean default true
);
insert into food_items (name, category, price, available)
values
('Dal Tadka', 'Main Course', 120, true),
('Roti', 'Bread', 15, true),
('Jeera Rice', 'Rice', 80, true),
('Paneer Sabzi', 'Main Course', 150, true);