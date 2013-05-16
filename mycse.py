# -*- coding: utf-8 -*-

import sys
import pgdb
import time

QUERY = []
DSN = []

ROW_LIMIT = 15

DIVIDER = '-----------------------'
QUERY_DIVIDER = '******************************'

class SelectDB():
  def select(self,con_file):

    f=open(con_file,'r')

    host = ''
    database = ''
    user = ''
    password = ''

    for line in f:
      paras = line.split('=')
      if paras[0].strip() == 'DATABASE_NAME':
        database = paras[1].strip()
      elif paras[0].strip() == 'DATABASE_USER':
        user = paras[1].strip()
      elif paras[0].strip() == 'DATABASE_PASS':
        password = paras[1].strip()
      elif paras[0].strip() == 'HOST':
        host= paras[1].strip()
    f.close()

    con_str = {'host':host,'database':database,'user':user,'password':password}
    return con_str

class SelectQuery():

  def select(self,sql_file):
    longline = ''
    f=open(sql_file,'r')
    for line in f:
      longline += line.replace('\n',' ')
    f.close()
    sqls = longline.split(';')
    sqls.pop()
    return sqls

class CheckerProcess():

  def __init__(self):
    self._con = pgdb.connect(**DSN) 
    self._cur = self._con.cursor() 

  def run(self,queries):
    end = 0
    for q in queries:
      print QUERY_DIVIDER
      print q
      print ''
      self._cur.execute(q)
      
      view = SqlViewer()

      head = self._cur.description 
      view.headShow(head) 

      result = self._cur.fetchall()
      view.rowShow(result)

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

class SqlViewer():
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
    argvs = sys.argv
    
    if len(argvs) < 2:
      print 'requires sql file'
      return

    global DSN 
    db_selecter = SelectDB()
    DSN=db_selecter.select('con.con')

    global QUERY
    qy_selecter = SelectQuery()
    QUERY=qy_selecter.select(argvs[1])

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

