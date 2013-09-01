select
grp_name,phn_nbr
from mst_group left join grp_phn on mst_group.grp_id = grp_phn.grp_id
