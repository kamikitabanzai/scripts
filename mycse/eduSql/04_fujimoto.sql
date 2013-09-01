SELECT grp_id,count(emp_id)
FROM emp_grp
Group by grp_id
order by grp_id;
