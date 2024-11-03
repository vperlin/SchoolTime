-- 
-- depends: 20241020_01_rOGSV-sclass-info

create view subgroups_by_subjects as
with
s0 as (
   select
         sg.iid,
         sg.iid_sclass,
         sg.title,
         sgs.iid_subject,
         sbj.code
      from subgroups as sg
      left outer join subgroups_subjects as sgs
         on sg.iid = sgs.iid_subgroup
      left outer join subjects as sbj
         on sgs.iid_subject = sbj.iid
      order by sgs.iid_subject
),
sgrp as (
   select
         iid,
         iid_sclass,
         title,
         array_agg(iid_subject) as iids_subject,
         string_agg(code, ', ') as codes_subject
      from s0
      group by iid, iid_sclass, title
),
s1 as (
   select
         array_agg(iid) as iids_subgroup,
         iid_sclass,
         string_agg(title, ', ') as titles_subgroup,
         iids_subject,
         codes_subject
      from sgrp
      group by iid_sclass, iids_subject, codes_subject
)
select
      b.iids_subgroup,
      b.iid_sclass,
      b.titles_subgroup,
      nullif(b.iids_subject, array[null::integer]) as iids_subject,
      b.codes_subject
  from s1 as b ;

grant select on subgroups_by_subjects to public ;
