Select
B.grp_name,
Count(B.grp_id)
from
emp_grp A
left join mst_group B on
A.grp_id = B.grp_id
Group By B.grp_id;
