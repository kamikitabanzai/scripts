# -*- coding: utf-8 -*-

import sys
import pgdb
import time

ROW_LIMIT = 10
COST_LIMIT = 10**7

DSN = {}

DIVIDER = '-----------------------'
QUERY_DIVIDER = '******************************'

INDEX_QUERY = 'select tablename , indexname , indexdef from pg_indexes where schemaname = \'public\''

class File():

  def returnDsn(self,conFile):
    buff = {}
    dsn = {}
    buff = self.conFile2buff(conFile)
    dsn = self.buff2dsn(buff)
    return dsn

  def buff2dsn(self,buff):
    dsn = {}
    dsn['host'] = buff['HOST']
    dsn['database'] = buff['DATABASE_NAME']
    dsn['user'] = buff['DATABASE_USER']
    dsn['password'] = buff['DATABASE_PASS']
    return dsn

  def conFile2buff(self,conFile):
    f=open(conFile,'r')
    buff = {}
    for line in f:
      if self.haveMeaning(line):
        paras = line.split('=')
        buff[paras[0].strip()] = paras[1].strip()
    f.close()
    return buff 

  def haveMeaning(self,line):
    if len(line.split('=')) <= 1:
      return False
    else:
      return True  

  def returnSqls(self,sqlFile):
    longLine = ''
    sqls = []
    longLine = self.sqlFile2longLine(sqlFile)
    sqls = self.longLine2sqls(longLine)
    return sqls

  def longLine2sqls(self,longLine):
    sqls = []
    sqls = longLine.split(';')
    sqls.pop()
    return sqls

  def sqlFile2longLine(self,sqlFile):
    longLine = ''
    f=open(sqlFile,'r')
    for line in f:
      longLine += line
    f.close()
    return longLine

class PgProcess():

  def __init__(self):
    self._con = pgdb.connect(**DSN) 
    self._cur = self._con.cursor() 

  def run(self,queries):
    end = 0
    total = Total()
    try:
      for q in queries:

        # まずcostが閾値以下であることを確認
        explainService = ExplainService()
        explain = explainService.exeExplain(q)
        if not explainService.checkCost(explain):
          continue
        
        start = time.time()
        self._cur.execute(q)
        each = time.time() - start
        end += each
        
        view = SqlViewer()
        view.each = each
        view.q = q
        view.explain = explain
        view.head = self._cur.description 
        view.result = self._cur.fetchall()

        view.view()

        total.each.append(each)

      total.end = end

      self._cur.execute(INDEX_QUERY)
      total.indexes = self._cur.fetchall()

      total.view()

    except :
      raise
    finally:
      self._con.close()
      self._cur.close()

    return

class Total():
  def __init__(self):
    self.each = []
    self.end = 0
    self.indexes = []
  
  def view(self):
    self.indexShow(self.indexes)
    self.totalShow()

  def indexShow(self,indexes):
    for i in indexes:
      print i
    print DIVIDER

  def totalShow(self):
    count = 0
    for e in self.each:
      count += 1
      print '[%s]:%.2f' % (count,e)
    print 'Total:%.2f sec' % self.end
    print ''

class ExplainService():

  def __init__(self):
    self._con = pgdb.connect(**DSN) 
    self._cur = self._con.cursor() 

  def exeExplain(self,sql):
    try:
      exp_q = 'explain ' + sql
      self._cur.execute(exp_q)
      exp_r = self._cur.fetchall()
    except:
      raise
    finally:
      self._con.close()
      self._cur.close()

    return exp_r

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
      if self.findCost(h): 
        cost = self.returnCost(h) 
        break
    return cost
  
  def findCost(self,line):
    if line.find('cost=') > 0:
      return True
    else:
      return False

  def returnCost(self,line):
    strCost = line.split('..')[1]
    return float(strCost)

class SqlViewer():

  def __init__(self):
    self.head = []
    self.result = []
    self.q = ''
    self.each = 0
    self.explain = []

  def view(self):
    self.queryShow(self.q) 
    self.headShow(self.head) 
    self.rowShow(self.result)
    self.expShow(self.explain)
    self.subShow()

  def queryShow(self,query):
    print ''
    print query

  def subShow(self):
    print DIVIDER
    print ' %d 行' % len(self.result)
    print ' %.2f sec' % self.each
    print QUERY_DIVIDER

  def expShow(self,explain):
    for exp in explain:
      print exp

  def headShow(self,heads):
    headOut = self.makeHead(heads)
    print headOut
  
  def makeHead(self,heads):
    headOut ='('
    for h in heads:
      if not headOut == '(':
        headOut += ','
      headOut += h[0]
    headOut +=')'
    return headOut
  
  def rowShow(self,rows):
    limiter = 0
    for row in rows:
      rowOut = self.makeRow(row)
      print rowOut

      limiter += 1
      if limiter >= ROW_LIMIT:
         break

  def makeRow(self,row):
    rowOut =' ['
    for column in row:
      if not rowOut == ' [':
        rowOut += ','

      if isinstance(column,str):
        rowOut += column #.decode('utf-8')
      else:
        rowOut += str(column)
    rowOut += ']'

    return rowOut

class MyCseService:
  def __init__(self,sqlFile):
    global DSN
    file= File()
    self.sqls = []
    DSN = file.returnDsn('con.con')
    self.sqls = file.returnSqls(sqlFile)
    self.pgprocess = PgProcess()

  def run(self):
    self.pgprocess.run(self.sqls)

def main():

  try:
    argvs = sys.argv
    
    if len(argvs) < 2:
      print 'requires sql file'
      return
    
    service = MyCseService(argvs[1]) 
    service.run()
    
  except Exception , e:
    print  e 
    import traceback
    print  traceback.format_exc() 
  except KeyboardInterrupt:
    print  'KeyboardInterrupt' 

if __name__ == '__main__':
    main()

