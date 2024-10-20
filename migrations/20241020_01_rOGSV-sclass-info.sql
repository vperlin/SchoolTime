-- SClass info
-- depends: 20240804_04_gqWXd-correcting-subject-privileges


create view sclass_info as
    select
            cl.iid as iid,
            cl.lyear as lyear,
            cl.letter as letter,
            cl.iid_leader as iid_leader,
            cl.note as note,
            tc.last_name || ' ' || tc.first_name || coalesce(' '||tc.middle_name,'') as name_leader,
            tc.phone as leader_phones
        from sclasses as cl
        left outer join teachers as tc
                on cl.iid_leader = tc.iid ;

grant select on sclass_info to public ;
