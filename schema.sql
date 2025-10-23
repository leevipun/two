create table users (
  id integer primary key,
  username text unique,
  password_hash text,
)

create table movies (
  id integer primary key,
  title text,
  description text,
  user_id integer references users,
  status varchar,
  created_at timestamp
)

create table reviews (
  id integer primary key,
  title varchar,
  body text,
  rating integer check (rating between 1 and 5),
  movie_id integer references movies,
  user_id integer references users
  created_at timestamp
)

create table pictures (
  id integer primary key,
  title varchar,
  alt varchar,
  movie_id integer references movies,
  created_at timestamp
)

create table categories (
  id integer primary key,
  name varchar
)

create table movie_categories (
  id integer primary key,
  movie_id integer references movies,
  category_id integer references categories,
  type text check (type in ('primary', 'secondary'))
)