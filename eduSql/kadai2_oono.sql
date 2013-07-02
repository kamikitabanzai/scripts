select emp_name,emp_kana,grp_name
from emp_grp a
left join mst_emp b
on a.emp_id = b.emp_id

left join mst_group c
on a.grp_id = c.grp_id;
