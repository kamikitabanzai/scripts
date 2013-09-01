#!/bin/bash
logdir=./log/`date +%Y%m%d`
loghead=`date +%H%M%S_`
conf=/etc/postgresql/9.2/main/postgresql.conf

if [ ! -d $logdir ]
then
  mkdir -p $logdir
fi

python mycse.py $1 | tee $logdir/${loghead}sql.log
cp $conf $logdir/${loghead}.conf

