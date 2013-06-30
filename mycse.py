# -*- coding: utf-8 -*-

import sys
import pgdb
import time

ROW_LIMIT = 10
COST_LIMIT = 10**7

DIVIDER = '-----------------------'
QUERY_DIVIDER = '******************************'

INDEX_QUERY = 'select tablename , indexname , indexdef from pg_indexes where schemaname = \'public\''

class File():

  def returnFromFile(self,obj,file):
    return obj.returnFromFile(file)

class DnsFileService():

  def returnFromFile(self,conFile):
    buff = {}
    dsn = {}
    buff = self.__conFile2buff(conFile)
    dsn = self.__buff2dsn(buff)
    return dsn

  def __conFile2buff(self,conFile):
    f=open(conFile,'r')
    buff = {}
    for line in f:
      if len(line.split('=')) > 1:
        paras = line.split('=')
        buff[paras[0].strip()] = paras[1].strip()
    f.close()
    return buff 

  def __buff2dsn(self,buff):
    dsn = {}
    dsn['host'] = buff['HOST']
    dsn['database'] = buff['DATABASE_NAME']
    dsn['user'] = buff['DATABASE_USER']
    dsn['password'] = buff['DATABASE_PASS']
    return dsn

class SqlFileService():

  def returnFromFile(self,sqlFile):
    longLine = ''
    sqls = []
    longLine = self.__sqlFile2longLine(sqlFile)
    sqls = self.__longLine2sqls(longLine)
    return sqls

  def __sqlFile2longLine(self,sqlFile):
    longLine = ''
    f=open(sqlFile,'r')
    for line in f:
      longLine += line
    f.close()
    return longLine

  def __longLine2sqls(self,longLine):
    sqls = []
    sqls = longLine.split(';')
    sqls.pop()
    return sqls

class PgProcess():

  def __init__(self,dsn,container):
    self.__con = pgdb.connect(**dsn) 
    self.__cur = self.__con.cursor() 
    self.__explainService = ExplainService(dsn)
    self.__container = container
    self.__qID = 0
    self.__totalTime = 0

  def run(self,sqls):
    try:
      self.__createSessionRunningSql(sqls)
    except :
      raise
    finally:
      self.__con.close()
      self.__cur.close()
    return

  def __createSessionRunningSql(self,sqls):
    for sql in sqls:
      self.__runSql(sql,self.__qID)
      self.__qID += 1
    self.__container.totalTime = self.__totalTime
    self.__cur.execute(INDEX_QUERY)
    self.__container.indexes = self.__cur.fetchall()
    return
  
  def __runSql(self,sql,qID):
    eachTime = self.__timeSql(sql)
    self.__totalTime += eachTime
    self.__container.eachTimes[qID] = eachTime
    self.__container.sqls[qID] = sql
    self.__container.plans[qID] = self.__explainService.getExplain(sql)
    self.__container.heads[qID] = self.__cur.description
    self.__container.results[qID] = self.__cur.fetchall()
    self.__container.qIDs.append(qID)
    return

  def __timeSql(self,sql):
    startTime = time.time()
    self.__cur.execute(sql)
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
 
  def showAllResult(self):
    for qID in self.qIDs:
      self.showOneResult(qID)
    return

  def showOneResult(self,qID):
    print ''
    print self.sqls[qID]
    headOut = self.__makeHead(self.heads[qID])
    print headOut
    self.__showResult(self.results[qID])
    print ''
    self.__showLines(self.plans[qID])
    print DIVIDER
    print ' %d 行' % len(self.results[qID])
    print ' %.2f sec' % self.eachTimes[qID]
    print QUERY_DIVIDER
 
  def showSummary(self):
    self.__showLines(self.indexes)
    print DIVIDER
    self.__showTotal(self.eachTimes,self.totalTime)
    print ''

  def __makeHead(self,heads):
    headOut ='('
    for h in heads:
      if not headOut == '(':
        headOut += ','
      headOut += h[0]
    headOut +=')'
    return headOut
  
  def __showResult(self,result):
    limiter = 0
    for row in result:
      rowOut = self.__makeRow(row)
      print rowOut
      limiter += 1
      if limiter >= ROW_LIMIT:
         break
    return

  def __makeRow(self,row):
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
  
  def __showLines(self,lines):
    for line in lines:
      print line
    return

  def __showTotal(self,eachTimes,totalTime):
    count = 0
    for eachTime in eachTimes.values():
      count += 1
      print '[%s]:%.2f' % (count,eachTime)
    print 'Total:%.2f sec' % totalTime

class ExplainService():

  def __init__(self,dsn):
    self.__con = pgdb.connect(**dsn) 
    self.__cur = self.__con.cursor() 
    self.enableSqls = []
 
  def cutHighCost(self,sqls):
    try:
      self.enableSqls = self.__createSessionCutHighCost(sqls)
    except:
      raise
    finally:
      self.__con.close()
      self.__cur.close()
    if len(self.enableSqls) < 1:
      raise NoEnableSql()
    return

  def __createSessionCutHighCost(self,sqls):
    enableSqls = []
    for sql in sqls:
      plan = self.getExplain(sql)
      cost = self.getCost(plan)
      if cost < COST_LIMIT:
        enableSqls.append(sql)
      else:
        __warnLimitOver(sql,cost)
    return enableSqls 

  def getExplain(self,sql):
    exp_q = 'explain ' + sql
    self.__cur.execute(exp_q)
    plan = self.__cur.fetchall()
    return plan

  def getCost(self,plan):
    header = plan[0][0].split(' ')
    cost = 0
    for h in header:
      if h.find('cost=') > 0:
        cost = float(h.split('..')[1]) 
        break
    return cost
  
  def __warnLimitOver(self,sql,cost):
    print 'this query dosn\'t'
    print DIVIDER
    print sql
    print DIVIDER
    print 'the cost of this query is over the limit cost=%.2f ' % (cost)
    return

class MyCseService:
  def __init__(self,sqlFile):
    dsn = {}
    self.sqls = []
    # ダックタイピングをしてみる(Javaでもインターフェース使って出来るよ！）
    file = File()
    dsn = file.returnFromFile(DnsFileService(),'con.con')
    self.sqls = file.returnFromFile(SqlFileService(),sqlFile)
    self.explainService = ExplainService(dsn)
    self.container = ResultContainer()
    # 実行結果はコンテナに格納する
    self.pgprocess = PgProcess(dsn,self.container)

  def run(self):
    # ヘビーSQLの削除
    self.explainService.cutHighCost(self.sqls)
    # SQLの実行
    enableSqls = self.explainService.enableSqls
    self.pgprocess.run(enableSqls)
    # 実行結果の出力
    self.container.showAllResult()
    self.container.showSummary()

class NoEnableSql(BaseException):
  def printException(self):
    print DIVIDER
    print "you have no enable sqls"

def main():
  argvs = sys.argv
  if len(argvs) < 2:
    print 'requires sql file'
    return
  try:
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

#start地点(pythonから最初に呼び出される)
if __name__ == '__main__':
    main()

