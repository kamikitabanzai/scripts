# -*- coding: utf-8 -*-

import sys
import pgdb
import time

QUERY = []
DSN = dict()

ROW_LIMIT = 10

DIVIDER = '-----------------------'
QUERY_DIVIDER = '******************************'

class GetDSN():
  def get(self,con_file):

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

class GetQuery():

  def get(self,sql_file):
    longline = ''
    f=open(sql_file,'r')
    for line in f:
      longline += line
    f.close()
    sqls = longline.split(';')
    sqls.pop()
    return sqls

class ExecuteProcess():

  def __init__(self):
    self._con = pgdb.connect(**DSN) 
    self._cur = self._con.cursor() 

  def run(self,queries):
    end = 0
    for q in queries:
      view = SqlViewer()

      view.q = q

      self._cur.execute(q)
      view.head = self._cur.description 
      view.result = self._cur.fetchall()

      #実行時間の取得（安定するよう2回目を計測）
      start = time.time()
      self._cur.execute(q)
      each = time.time() - start
      end += each
      view.each = each
      
      exp_q = 'explain ' + q
      self._cur.execute(exp_q)
      view.explain = self._cur.fetchall()

      view.view()
    print '計:%.2f sec' % end
    print ''
    
    self._cur.close()
    self._con.close()

    return

class SqlViewer():
  head = []
  result = []
  q = ''
  each = 0
  explain = []

  def view(self):
      print self.q
      print ''
      
      self.headShow(self.head) 
      self.rowShow(self.result)

      print DIVIDER
      print ' %d 行' % len(self.result)
      print ' %.2f sec' % self.each

      for exp in self.explain:
        print exp

      print QUERY_DIVIDER

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
    db_getter = GetDSN()
    DSN=db_getter.get('con.con')

    global QUERY
    qy_getter = GetQuery()
    QUERY=qy_getter.get(argvs[1])

    pgprocess = ExecuteProcess()
    pgprocess.run(QUERY)
    
  except Exception , e:
    print  e 
    import traceback
    print  traceback.format_exc() 
  except KeyboardInterrupt:
    print  'KeyboardInterrupt' 

if __name__ == '__main__':
    main()

