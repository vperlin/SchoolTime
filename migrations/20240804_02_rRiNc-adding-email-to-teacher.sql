-- Adding email to teacher
-- depends: 20240804_01_ViPpv-teachers-and-subjects

alter table teachers
   add column email text ;
