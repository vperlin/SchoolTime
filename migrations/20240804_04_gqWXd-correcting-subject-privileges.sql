-- Correcting subject privileges
-- depends: 20240804_03_RyCJg-adding-emailto-teachers-info

grant insert, update on subjects to public ;
grant usage on sequence subjects_iid_seq to public ;

grant insert, update on teachers to public ;
grant usage on sequence teachers_iid_seq to public ;

grant insert, delete on teachers_subjects to public ;

grant select, insert, update on sclasses to public ;
grant usage on sequence sclasses_iid_seq to public ;
