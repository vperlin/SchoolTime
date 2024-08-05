-- Correcting subject privileges
-- depends: 20240804_03_RyCJg-adding-emailto-teachers-info

revoke insert, update on subjects from public ;
revoke usage on sequence subjects_iid_seq from public ;
