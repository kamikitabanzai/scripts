select
A.grp_name
,B.phn_nbr
from
mst_group A
left join grp_phn B 
on A.grp_id = B. grp_id;

