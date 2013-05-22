   SELECT COUNT(*)
     FROM page
     JOIN revision
       ON page_id = rev_page
    WHERE page_is_redirect = 0
      AND page_namespace = 0
      AND rev_user = 0
        ;

   SELECT COUNT(*)
     FROM page
     JOIN revision
       ON page_id = rev_page
    WHERE page_is_redirect = 0
      AND page_namespace = 0
      AND rev_user = 0
      AND page_touched > 
              to_char(date_trunc('year',NOW() - INTERVAL '1 YEAR')
                      ,'yyyymmddhh24miss')
        ;

   SELECT page_id
     FROM page
     JOIN revision
       ON page_id = rev_page
    WHERE page_is_redirect = 0
      AND page_namespace = 0
      AND rev_user = 0
 ORDER BY page_touched DESC
    LIMIT 10
        ;

   SELECT rev_user,count(*) AS c
     FROM page
     JOIN revision
       ON page_id = rev_page
    WHERE page_is_redirect = 0
      AND page_namespace = 0
 GROUP BY rev_user
 ORDER BY c DESC
        ;

   SELECT SUBSTRING(rev_timestamp,1,6),count(*) AS c
     FROM page
     JOIN revision
       ON page_id = rev_page
    WHERE page_is_redirect = 0
      AND page_namespace = 0
 GROUP BY SUBSTRING(rev_timestamp,1,6)
 ORDER BY c DESC
        ;

