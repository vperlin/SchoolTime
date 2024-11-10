-- Adjust privileges
-- depends: 20241103_01_mCsCA

grant select, insert, update on subgroups to public ;
grant usage on sequence subgroups_iid_seq to public ;

grant select, insert, delete on subgroups_students to public ;
grant select, insert, delete on subgroups_subjects to public ;
