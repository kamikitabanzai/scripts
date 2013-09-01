select
A.emp_name,
C.grp_name
from
mst_emp A
left join emp_grp B on
A.emp_id = B.emp_id
left join mst_group C on
B.grp_id = C.grp_id;
