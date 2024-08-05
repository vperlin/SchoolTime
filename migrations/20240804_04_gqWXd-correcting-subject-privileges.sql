-- Correcting subject privileges
-- depends: 20240804_03_RyCJg-adding-emailto-teachers-info

grant insert, update on subjects to public ;
grant usage on sequence subjects_iid_seq to public ;
