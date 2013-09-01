--シングル用　直近二世代取得

set pages 0
spool awr_tmp.sql
 select 
 'define report_type=text' || chr(10) ||
 'define num_days=2' || chr(10) ||
 'define begin_snap='  || SNAP_ID      || chr(10) ||
 'define end_snap='    || (SNAP_ID + 1)|| chr(10) ||
 'define report_name=' || SNAP_ID || '_' || (SNAP_ID + 1) || '.txt' || chr(10) ||
 '@?/rdbms/admin/awrrpt.sql' || chr(10)
 from sys.dba_hist_snapshot
 where snap_id > (select max(snap_id)-3 from sys.dba_hist_snapshot)
   and snap_id < (select max(snap_id) from sys.dba_hist_snapshot)
 order by snap_id;
spool off
--@awr_tmp.sql

exit
