-- Adjust student
-- depends: 20241110_01_j7Xs5-adjust-privileges

alter table students
    add column gender boolean ;

alter table students
    add column birth_date date ;
