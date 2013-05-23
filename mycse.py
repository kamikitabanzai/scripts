# -*- coding: utf-8 -*-

import sys
import pgdb
import time

QUERY = []
DSN = dict()

ROW_LIMIT = 10
COST_LIMIT = 10**7

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
    total = Total()
    for q in queries:

      # まずcostが閾値以下であることを確認
      exp_q = 'explain ' + q
      self._cur.execute(exp_q)
      exp_r = self._cur.fetchall()

      sqlexplain = SqlExplain()
      if not sqlexplain.checkCost(exp_r):
        continue
      
      # SQLを実行し出力
      view = SqlViewer()
      view.q = q
      view.explain = exp_r 
      self._cur.execute(q)
      view.head = self._cur.description 
      view.result = self._cur.fetchall()

      #実行時間の取得（安定するよう2回目を計測）
      start = time.time()
      self._cur.execute(q)
      each = time.time() - start
      end += each
      view.each = each
      
      view.view()

      total.each.append(each)

    total.end = end
    total.totalShow()

    self._cur.close()
    self._con.close()

    return

class Total():
  each = []
  end = 0

  def totalShow(self):
    count = 0
    for e in self.each:
      count += 1
      print '[%s]:%.2f' % (count,e)
    print 'Total:%.2f sec' % self.end
    print ''

class SqlExplain():

  def checkCost(self,explain):
    cost = self.getCost(explain)

    if cost < COST_LIMIT:
      return True
    else:
      print 'cost=%.2f the cost of this query is over the limit' % (cost)
      return False

  def getCost(self,explain):
    header = explain[0][0].split(' ')
    cost = 0
    for h in header:
      if h.find('cost=') > 0:
        strCost = h.split('..')[1]
        cost = float(strCost)
    return cost

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

      for exp in self.explain:
        print exp

      print DIVIDER
      print ' %d 行' % len(self.result)
      print ' %.2f sec' % self.each

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
      #str型を文字コード変換しないとバイナリで出力される
      rowOut =' ['
      for column in row:
        if not rowOut == ' [':
          rowOut += ','

        if isinstance(column,str):
          rowOut += column #.decode('utf-8')
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

