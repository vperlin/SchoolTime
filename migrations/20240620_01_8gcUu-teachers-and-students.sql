-- Teachers and Students
-- depends: 

create table teachers (
    iid serial not null primary key,
    last_name text not null,
    first_name text not null,
    middle_name text,
    phone text,
    note text
) ;

create table students (
    iid serial not null primary key,
    last_name text not null,
    first_name text not null,
    middle_name text,
    phone text,
    phone_parents text,
    note text
) ;
