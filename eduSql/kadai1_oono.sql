select grp_name,phn_nbr from mst_group a
left join grp_phn b
on a.grp_id = b.grp_id;

