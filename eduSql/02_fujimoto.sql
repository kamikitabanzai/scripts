SELECT emp_name,grp_name FROM mst_emp a left join emp_grp b on a.emp_id = b.emp_id
left join mst_group c on b.grp_id = c.grp_id;
