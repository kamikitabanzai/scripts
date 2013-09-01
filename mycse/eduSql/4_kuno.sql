select 
	count(emp_id)
	,grp_name 
from emp_grp a 
left join mst_group b on a.grp_id = b.grp_id
GROUP BY grp_name;
