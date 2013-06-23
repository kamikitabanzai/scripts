select count(distinct new_zip_id) as varaety
,pref 
from mst_zip 
group by pref 
order by varaety
;
