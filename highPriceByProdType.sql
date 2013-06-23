select p1.prod_name
  ,p1.price
from mst_prod as p1
where p1.price = (
  select max(p2.price) 
  from mst_prod as p2 
  where p1.prod_type_id=p2.prod_type_id
)
;
