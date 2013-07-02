select count(a.new_zip_id), a.pref
from (
  select new_zip_id,pref
  from mst_zip
  group by new_zip_id,pref
  order by new_zip_id
) a
group by a.pref
order by count(a.new_zip_id)
;

