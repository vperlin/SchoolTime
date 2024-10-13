-- Correcting subject privileges
-- depends: 20240804_03_RyCJg-adding-emailto-teachers-info

revoke insert, update on subjects from public ;
revoke usage on sequence subjects_iid_seq from public ;

revoke insert, update on teachers from public ;
revoke usage on sequence teachers_iid_seq from public ;

revoke insert, delete on teachers_subjects from public ;

revoke select, insert, update on sclasses from public ;
revoke usage on sequence sclasses_iid_seq from public ;
