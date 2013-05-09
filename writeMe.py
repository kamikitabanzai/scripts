# -*- coding: utf-8 -*-

import pgdb
import time

DATABASE_NAME = 'ossdb'
DATABASE_USER = 'postgres'
DATABASE_PASS = 'postgres'
HOST = '127.0.0.1'

ROW_LIMIT = 5

DIVIDER = '-----------------------'
QUERY_DIVIDER = '******************************'
QUERY = [
  '''
    SELECT 
     *
    FROM 
     prod
  '''
  ,'''
    SELECT
     *
    FROM
     customer
  '''
]

class CheckerProcess():

  def __init__(self):
    self._con = pgdb.connect(host=HOST,database=DATABASE_NAME,user=DATABASE_USER,password=DATABASE_PASS)
    self._cur = self._con.cursor()

  def run(self):
    end = 0
    for q in QUERY:
      print q

      start = time.time()
      self._cur.execute(q)
      each = time.time() - start
      end += each
      
      result = self._cur.fetchall()
      limiter = 0
      for row in result:

        limiter += 1
        if limiter > ROW_LIMIT:
          break

        rowOut =' ['
        for column in row:
          
          if not rowOut == ' [':
            rowOut += ','
          if not isinstance(column,int):
            rowOut += column.decode('utf-8')
          else:
            rowOut += str(column)
        rowOut += ']'
        print rowOut
      print DIVIDER
      print ' %d 行' % len(result)
      print ' %.5f sec' % each
      print QUERY_DIVIDER
    print '計:%.5f sec' % end
    print ''
    
    self._cur.close()
    self._con.close()

    return

def main():
  
  checker = CheckerProcess()

  try:
    checker.run()
    
  except Exception , e:
    print  e 
    import traceback
    print  traceback.format_exc() 
  except KeyboardInterrupt:
    print  'KeyboardInterrupt' 

if __name__ == '__main__':
    main()

