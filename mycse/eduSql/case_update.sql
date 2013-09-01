begin;
update mst_prod 
set price = 
	case when prod_type_id = '01'
		then price * 1.1
             when prod_type_id = '02'
		then price * 1.2
	      else price end
;
rollback;
