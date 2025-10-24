create table users (
  id SERIAL primary key,
  username text unique,
  password_hash text
);

create table movies (
  id SERIAL primary key,
  title text NOT NULL,
  year integer,
  duration integer,
  director text,
  genre varchar(50),
  watch_date date,
  rating decimal(3,1) check (rating between 1 and 10),
  watched_with text,
  platform varchar(50),
  review text,
  favorite boolean DEFAULT false,
  rewatchable boolean DEFAULT false,
  user_id integer references users,
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

create table user_favorites (
  id SERIAL primary key,
  user_id integer references users,
  movie_id integer references movies,  
  created_at timestamp DEFAULT CURRENT_TIMESTAMP,
  UNIQUE(user_id, movie_id)
);