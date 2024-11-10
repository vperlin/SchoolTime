-- Adjust privileges
-- depends: 20241103_01_mCsCA

revoke select, insert, update on subgroups from public ;
revoke usage on sequence subgroups_iid_seq from public ;


revoke select, insert, delete on subgroups_students from public ;
revoke select, insert, delete on subgroups_subjects from public ;
