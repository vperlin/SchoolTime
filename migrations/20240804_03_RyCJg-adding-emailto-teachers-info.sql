-- Adding emailto teachers_info
-- depends: 20240804_02_rRiNc-adding-email-to-teacher

create view teachers_info1 as
with sbj as (
	select
    	  iid_teacher,
      	  array_agg(iid_subject) as subjects
       from teachers_subjects
       group by iid_teacher
)
select
	  tc.iid,
	  tc.last_name,
	  tc.first_name,
	  tc.middle_name,
	  tc.phone,
	  tc.email,
	  tc.note,
	  coalesce(sbj.subjects, array[]::int[]) as subjects,
	  NULL as lead_group
    from teachers as tc
    left outer join sbj
       on sbj.iid_teacher = tc.iid ;

grant select on teachers_info1 to public ;
