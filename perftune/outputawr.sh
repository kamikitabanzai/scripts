#!/bin/sh

LOG_DIR=log
BASE_DIR=`dirname $0`

if [ ! -d "${BASE_DIR}/${LOG_DIR}" ]
then
	mkdir "${BASE_DIR}/${LOG_DIR}"
fi

cd "${BASE_DIR}/${LOG_DIR}"
sqlplus system/password@../outputawr.sql
