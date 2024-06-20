-- Classes and Subjects
-- depends: 20240620_01_8gcUu-teachers-and-students

create table sclasses (
    iid serial not null primary key,
    lyear int not null,
    letter text,
    iid_leader int references teachers(iid),
    note text
) ;

alter table students
   add column iid_sclass int not null references sclasses(iid) ;


create table subjects (
    iid serial not null primary key,
    code text not null unique,
    title text,
    note text
) ;

create table teachers_subjects(
    iid_teacher int not null references teachers(iid),
    iid_subject int not null references subjects(iid),
    constraint teachers_subjects_pkey primary key ( iid_teacher, iid_subject)
) ;
