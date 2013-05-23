# -*- coding: utf-8 -*-

import pgdb

DATABASE_NAME = 'yaoya'
DATABASE_USER = 'postgres'
DATABASE_PASS = 'postgres'
HOST = '127.0.0.1'

QUERY = [
  '''
    SELECT 
     *
    FROM 
     mst_prod
  '''
]

class CheckerProcess():

  def __init__(self):
    self._con = pgdb.connect(host=HOST,database=DATABASE_NAME,user=DATABASE_USER,password=DATABASE_PASS)
    self._cur = self._con.cursor()

  def run(self,queries):
    for q in queries:
      self._cur.execute(q)
      rows = self._cur.fetchall()
      print rows[0][0]

    self._cur.close()
    self._con.close()
    return

def main():
  
  checker = CheckerProcess()

  try:
    checker.run(QUERY)
    
  except Exception , e:
    print  e 
    import traceback
    print  traceback.format_exc() 
  except KeyboardInterrupt:
    print  'KeyboardInterrupt' 

if __name__ == '__main__':
    main()

