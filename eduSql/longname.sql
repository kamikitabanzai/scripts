select
  new_zip_id
  ,char_length(area)
  ,char_length(area_kana)
  ,area
  ,area_kana
from mst_zip
where new_zip_id in
(
  select
    a.new_zip_id
  from mst_zip a
    left outer join mst_zip b
      on a.new_zip_id = b.new_zip_id
         and a.order_id < b.order_id
  where
    b.order_id is not null
    and a.r_bigarea_flg = false
    and a.r_smallarea_flg = false
)
;

