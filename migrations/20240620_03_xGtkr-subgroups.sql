-- Subgroups
-- depends: 20240620_02_MKLUT-classes-and-subjects


create table subgroups (
    iid serial not null primary key,
    title text not null,
    iid_sclass int not null references sclasses(iid),
    note text
) ;

create table subgroups_students (
    iid_subgroup int not null references subgroups(iid),
    iid_student int not null references students(iid),
    constraint subgroups_students_pkey primary key(iid_subgroup, iid_student)
) ;

create table subgroups_subjects (
    iid_subgroup int not null references subgroups(iid),
    iid_subject int not null references subjects(iid),
    constraint subgroups_subjects_pkey primary key(iid_subgroup, iid_subject)
) ;


create table metagroups (
    iid serial not null primary key,
    title text not null,
    note text
) ;

create table metagroups_students (
    iid_metagroup int not null references metagroups(iid),
    iid_student int not null references students(iid),
    constraint metagroups_students_pkey primary key(iid_metagroup, iid_student)
) ;

create table metagroups_subjects (
    iid_metagroup int not null references metagroups(iid),
    iid_subject int not null references subjects(iid),
    constraint metagroups_subjects_pkey primary key(iid_metagroup, iid_subject)
) ;
