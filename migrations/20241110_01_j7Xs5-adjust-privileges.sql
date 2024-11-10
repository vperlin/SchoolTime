-- Adjust privileges
-- depends: 20241103_01_mCsCA

grant select, insert, update on subgroups to public ;
grant usage on sequence subgroups_iid_seq to public ;
