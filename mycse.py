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

  def conFile2buff(self,conFile):
    f=open(conFile,'r')
    buff = {}
    for line in f:
      if len(line.split('=')) > 1:
        paras = line.split('=')
        buff[paras[0].strip()] = paras[1].strip()
    f.close()
    return buff 

  def buff2dsn(self,buff):
    dsn = {}
    dsn['host'] = buff['HOST']
    dsn['database'] = buff['DATABASE_NAME']
    dsn['user'] = buff['DATABASE_USER']
    dsn['password'] = buff['DATABASE_PASS']
    return dsn

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

  def __init__(self,container):
    self._con = pgdb.connect(**DSN) 
    self._cur = self._con.cursor() 
    self.explainService = ExplainService()
    self.container = container
    self.qID = 0
    self.totalTime = 0

  def run(self,sqls):
    try:
      self.createSessionRunningSql(sqls)
    except :
      raise
    finally:
      self._con.close()
      self._cur.close()
    return

  def createSessionRunningSql(self,sqls):
    for sql in sqls:
      self.runSql(sql,self.qID)
      self.container.showOneResult(self.qID)
      self.qID += 1
    self.container.totalTime = self.totalTime
    self._cur.execute(INDEX_QUERY)
    self.container.indexes = self._cur.fetchall()
    return
  
  def runSql(self,sql,qID):
    eachTime = self.timeSql(sql)
    self.totalTime += eachTime
    self.container.eachTimes[qID] = eachTime
    self.container.sqls[qID] = sql
    self.container.plans[qID] = self.explainService.getExplain(sql)
    self.container.heads[qID] = self._cur.description
    self.container.results[qID] = self._cur.fetchall()
    self.container.qIDs.append(qID)

  def timeSql(self,sql):
    startTime = time.time()
    self._cur.execute(sql)
    eachTime = time.time() - startTime
    return eachTime

class ResultContainer():
  def __init__(self):
    self.qIDs = []
    self.heads = {}
    self.sqls = {}
    self.results = {}
    self.plans = {}
    self.eachTimes = {}
    self.totalTime = 0
    self.indexes = []
  
  def showOneResult(self,qID):
    print ''
    print self.sqls[qID]
    headOut = self.makeHead(self.heads[qID])
    print headOut
    self.showResult(self.results[qID])
    print ''
    self.showLines(self.plans[qID])
    print DIVIDER
    print ' %d 行' % len(self.results[qID])
    print ' %.2f sec' % self.eachTimes[qID]
    print QUERY_DIVIDER
 
  def showSummary(self):
    self.showLines(self.indexes)
    print DIVIDER
    self.showTotal(self.eachTimes,self.totalTime)
    print ''

  def makeHead(self,heads):
    headOut ='('
    for h in heads:
      if not headOut == '(':
        headOut += ','
      headOut += h[0]
    headOut +=')'
    return headOut
  
  def showResult(self,result):
    limiter = 0
    for row in result:
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
  
  def showLines(self,lines):
    for line in lines:
      print line
    return

  def showTotal(self,eachTimes,totalTime):
    count = 0
    for eachTime in eachTimes.values():
      count += 1
      print '[%s]:%.2f' % (count,eachTime)
    print 'Total:%.2f sec' % totalTime

class ExplainService():

  def __init__(self):
    self._con = pgdb.connect(**DSN) 
    self._cur = self._con.cursor() 
    self.enableSqls = []
 
  def cutHighCost(self,sqls):
    try:
      self.enableSqls = self.createSessionCutHighCost(sqls)
    except:
      raise
    finally:
      self._con.close()
      self._cur.close()
    if len(self.enableSqls) < 1:
      raise NoEnableSql()
    return

  def createSessionCutHighCost(self,sqls):
    enableSqls = []
    for sql in sqls:
      plan = self.getExplain(sql)
      cost = self.getCost(plan)
      if cost < COST_LIMIT:
        enableSqls.append(sql)
      else:
        warnLimitOver(sql,cost)
    return enableSqls 

  def getExplain(self,sql):
    exp_q = 'explain ' + sql
    self._cur.execute(exp_q)
    plan = self._cur.fetchall()
    return plan

  def getCost(self,plan):
    header = plan[0][0].split(' ')
    cost = 0
    for h in header:
      if h.find('cost=') > 0:
        cost = float(h.split('..')[1]) 
        break
    return cost
  
  def warnLimitOver(self,sql,cost):
    print 'this query dosn\'t'
    print DIVIDER
    print sql
    print DIVIDER
    print 'the cost of this query is over the limit cost=%.2f ' % (cost)
    return

class MyCseService:
  def __init__(self,sqlFile):
    global DSN
    file = File()
    self.sqls = []
    DSN = file.returnDsn('con.con')
    self.sqls = file.returnSqls(sqlFile)
    self.explainService = ExplainService()
    self.container = ResultContainer()
    # 実行結果をコンテナに格納する
    self.pgprocess = PgProcess(self.container)

  def run(self):
    # ヘビーSQLの削除
    self.explainService.cutHighCost(self.sqls)
    # SQLの実行と結果の出力
    enableSqls = self.explainService.enableSqls
    self.pgprocess.run(enableSqls)
    # 実行結果まとめの出力
    self.container.showSummary()

class NoEnableSql(BaseException):
  def printException(self):
    print DIVIDER
    print "you have no enable sqls"

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
  except NoEnableSql, E:
    E.printException()

if __name__ == '__main__':
    main()

