create table users (
  id SERIAL primary key,
  username text unique,
  password_hash text
);

create table movies (
  id SERIAL primary key,
  title text,
  description text,
  user_id integer references users,
  status varchar(50),
  created_at timestamp DEFAULT CURRENT_TIMESTAMP
);

create table reviews (
  id SERIAL primary key,
  title varchar(255),
  body text,
  rating integer check (rating between 1 and 5),
  movie_id integer references movies,
  user_id integer references users,
  created_at timestamp DEFAULT CURRENT_TIMESTAMP
);

create table pictures (
  id SERIAL primary key,
  title varchar(255),
  alt varchar(255),
  movie_id integer references movies,
  created_at timestamp DEFAULT CURRENT_TIMESTAMP
);

create table categories (
  id SERIAL primary key,
  name varchar(100)
);

create table movie_categories (
  id SERIAL primary key,
  movie_id integer references movies,
  category_id integer references categories,
  type varchar(10) check (type in ('primary', 'secondary'))
);