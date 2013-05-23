# -*- coding: utf-8 -*-

import pgdb

DATABASE_NAME = ''
DATABASE_USER = ''
DATABASE_PASS = ''
HOST = ''

class DSNGet():

  def run(self):
    f=open('con.con','r')
    global DATABASE_NAME
    global DATABASE_USER
    global DATABASE_PASS
    global HOST

    for line in f:
      paras = line.split('=')
      if paras[0].strip() == 'DATABASE_NAME':
        DATABASE_NAME = paras[1].strip()
      elif paras[0].strip() == 'DATABASE_USER':
        DATABASE_USER = paras[1].strip()
      elif paras[0].strip() == 'DATABASE_PASS':
        DATABASE_PASS = paras[1].strip()
      elif paras[0].strip() == 'HOST':
        HOST = paras[1].strip()

class GoProcess():

  def __init__(self):
    self._con = pgdb.connect(host=HOST,database=DATABASE_NAME,user=DATABASE_USER,password=DATABASE_PASS)
    self._cur = self._con.cursor()

  def run(self):
     
    query = [ 
      '''
        SELECT 
         *
        FROM mst_prod
      '''
      ,
      '''
        select * from mst_supp
      '''
    ]

    for q in query:
      self._cur.execute(q)
      rows = self._cur.fetchall()
      print rows[0][0]
      print rows[1][0]

    self._cur.close()
    self._con.close()
    return

def main():
  
  getter = DSNGet()

  try:
    getter = DSNGet()
    getter.run()

    go = GoProcess()
    go.run()
    
  except Exception , e:
    print  e 
    import traceback
    print  traceback.format_exc() 
  except KeyboardInterrupt:
    print  'KeyboardInterrupt' 

if __name__ == '__main__':
    main()

