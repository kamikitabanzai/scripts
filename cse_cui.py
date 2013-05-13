# -*- coding: utf-8 -*-

import pgdb
import time

DATABASE_NAME = ''
DATABASE_USER = ''
DATABASE_PASS = ''
HOST = ''

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
     supp
  '''
]

class SelectDB():
  def select(self):
    f=open('con.con','r')
    for line in f:
      paras = line.split('=')
      if paras[0].strip() == 'DATABASE_NAME':
        global DATABASE_NAME
        DATABASE_NAME = paras[1].strip()
      elif paras[0].strip() == 'DATABASE_USER':
        global DATABASE_USER
        DATABASE_USER = paras[1].strip()
      elif paras[0].strip() == 'DATABASE_PASS':
        global DATABASE_PASS
        DATABASE_PASS = paras[1].strip()
      elif paras[0].strip() == 'HOST':
        global HOST
        HOST = paras[1].strip()
    f.close()

class CheckerProcess():

  def __init__(self):
    self._con = pgdb.connect(host=HOST,database=DATABASE_NAME,user=DATABASE_USER,password=DATABASE_PASS)
    self._cur = self._con.cursor()

  def run(self,queries):
    end = 0
    for q in queries:
      print q

      self._cur.execute(q)

      head = self._cur.description 
      self.headShow(head) 

      result = self._cur.fetchall()
      self.rowShow(result)

      print DIVIDER
      print ' %d 行' % len(result)
      
      #実行時間は2回目を出力
      start = time.time()
      self._cur.execute(q)
      each = time.time() - start
      end += each
     
      print ' %.5f sec' % each
      print QUERY_DIVIDER
    print '計:%.5f sec' % end
    print ''
    
    self._cur.close()
    self._con.close()

    return

  def headShow(self,heads):
    headOut ='('
    for h in heads:
      if not headOut == '(':
        headOut += ','
      headOut += h[0]
    headOut +=')'
    print headOut

  def rowShow(self,rows):
    limiter = 0
    for row in rows:

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

def main():

  try:
    selecter = SelectDB()
    selecter.select()

    checker = CheckerProcess()
    checker.run(QUERY)
    
  except Exception , e:
    print  e 
    import traceback
    print  traceback.format_exc() 
  except KeyboardInterrupt:
    print  'KeyboardInterrupt' 

if __name__ == '__main__':
    main()

