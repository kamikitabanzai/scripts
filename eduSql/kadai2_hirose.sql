select
emp_name,emp_kana,grp_name
from mst_emp a right join emp_grp b on a.emp_id = b.emp_id
left join mst_group c on b.grp_id = c.grp_id;
