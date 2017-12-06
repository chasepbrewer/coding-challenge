create table widgets (
  id integer primary key,
  amount integer default 0
);

create table widget_types (
  widget_id integer primary key,
  name varchar(255) not null,
  foreign key (widget_id) references widget(id)
);

create table widget_sizes (
  id integer primary key,
  name varchar(255)
);

create table widget_finishes (
  id integer primary key,
  name varchar(255)
);

create table widget_size_map (
  widget_id integer not null,
  widget_size_id integer not null,
  foreign key (widget_id) references widgets(id),
  foreign key (widget_size_id) references widget_sizes(id),
  primary key (widget_id, widget_size_id)
);

create table widget_finish_map (
  widget_id integer not null,
  widget_finish_id integer not null,
  foreign key (widget_id) references widgets(id),
  foreign key (widget_finish_id) references widget_finishes(id),
  primary key (widget_id, widget_finish_id)
);

create table orders (
  id integer primary key
);

create table order_widgets (
  order_id integer not null,
  widget_id integer not null,
  widget_size_id integer not null,
  widget_finish_id integer not null,
  amount integer default 1,
  foreign key (order_id) references orders(id),
  foreign key (widget_id) references widgets(id),
  foreign key (widget_size_id) references widget_sizes(id),
  foreign key (widget_finish_id) references widget_finishes(id),
  primary key (order_id, widget_id)
);

insert into widget_sizes (name) values ('Small'), ('Medium'), ('Large');
insert into widget_finishes (name) values ('Chrome'), ('Wood'), ('Blue');
insert into widgets (amount) values (36), (24), (13);
insert into widget_types (
  widget_id,
  name)
values
  (1, 'Prime'),
  (2, 'Super'),
  (3, 'Mega');

insert into widget_size_map (
  widget_id,
  widget_size_id)
values
  (1, 1),
  (2, 1),
  (2, 2),
  (3, 1),
  (3, 2),
  (3, 3);

insert into widget_finish_map (
  widget_id,
  widget_finish_id
) values
  (1, 1),
  (2, 1),
  (2, 2),
  (3, 1),
  (3, 2),
  (3, 3);
