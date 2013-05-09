import time
import pgdb

DATABASE_NAME = 'wikipedia'
DATABASE_USER = 'postgres'
DATABASE_PASS = 'postgres'
HOST = '127.0.0.1'

QUERY = [
	'''
            SELECT COUNT(*)
              FROM page
              JOIN revision
                ON page_id = rev_page
             WHERE page_is_redirect = 0
               AND page_namespace = 0
               AND rev_user = 0
        ''',
        '''
            SELECT COUNT(*)
              FROM page
              JOIN revision
                ON page_id = rev_page
             WHERE page_is_redirect = 0
               AND page_namespace = 0
               AND rev_user = 0
               AND page_touched > to_char(date_trunc('year',NOW() - INTERVAL '1 YEAR'),'yyyymmddhh24miss')
        ''',
	'''
            SELECT page_id
              FROM page
              JOIN revision
                ON page_id = rev_page
             WHERE page_is_redirect = 0
               AND page_namespace = 0
               AND rev_user = 0
          ORDER BY page_touched DESC
             LIMIT 10
        ''',
        '''
            SELECT rev_user,count(*) AS c
              FROM page
              JOIN revision
                ON page_id = rev_page
             WHERE page_is_redirect = 0
               AND page_namespace = 0
          GROUP BY rev_user
          ORDER BY c DESC
        ''',
        '''
            SELECT SUBSTRING(rev_timestamp,1,6),count(*) AS c
              FROM page
              JOIN revision
                ON page_id = rev_page
             WHERE page_is_redirect = 0
               AND page_namespace = 0
          GROUP BY SUBSTRING(rev_timestamp,1,6)
          ORDER BY c DESC
        ''',
]

class CheckerProcess():

  def __init__(self):
    self._con = pgdb.connect(host=HOST,database=DATABASE_NAME,user=DATABASE_USER,password=DATABASE_PASS)
    self._cur = self._con.cursor()

  def run(self):
    start = time.time()

    for q in QUERY:
        each = time.time()
        self._cur.execute(q)
        print time.time() - each

    end = time.time()
    elapsed = end - start
    return elapsed

def main():
  
  checker = CheckerProcess()

  try:
    s = checker.run()
    print "Total:%.5f" % s
    
  except Exception, e:
    print e
    import traceback
    print traceback.format_exc()
  except KeyboardInterrupt:
    print 'KeyboardInterrupt'

if __name__ == '__main__':
    main()

