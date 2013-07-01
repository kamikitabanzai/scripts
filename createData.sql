delete from emp_grp;
delete from grp_phn;
delete from mst_group;
delete from mst_emp;

drop table emp_grp;
drop table grp_phn;
drop table mst_group;
drop table mst_emp;

create table mst_emp(
  emp_id char(5)
  ,emp_name varchar(50)
  ,emp_kana varchar(50)
  ,mail varchar(50)
)
;

create table mst_group(
  grp_id char(2)
  ,grp_name varchar(50)
)
;

alter table mst_emp add primary key(emp_id);
alter table mst_group add primary key(grp_id);

create table emp_grp(
  emp_id char(5)
  ,grp_id char(2)
)
;

alter table emp_grp add primary key (emp_id,grp_id);
alter table emp_grp add foreign key (emp_id) references mst_emp;
alter table emp_grp add foreign key (grp_id) references mst_group;

create table grp_phn(
  grp_id char(2)
  ,phn_nbr char(20)
)
;
alter table grp_phn add primary key (grp_id,phn_nbr);
alter table grp_phn add foreign key (grp_id) references mst_group;

begin;
insert into mst_emp values('00001','大野結衣','オオノユイ','abc@def.com');
insert into mst_emp values('00002','河野和希','コウノカズキ','abc@def.com');
insert into mst_emp values('00003','久野翔平','クノショウヘイ','abc@def.com');
insert into mst_emp values('00004','廣瀬由幸','ヒロセヨシユキ','abc@def.com');
insert into mst_emp values('00005','藤本愛也','フジモトマナヤ','abc@def.com');

insert into mst_group values('01','インフラソリューショングループ');
insert into mst_group values('02','ビジネスデザイングループ');
insert into mst_group values('03','産業システムグループ');

insert into emp_grp values('00001','01');
insert into emp_grp values('00002','02');
insert into emp_grp values('00003','03');
insert into emp_grp values('00004','01');
insert into emp_grp values('00005','02');
insert into emp_grp values('00005','03');

insert into grp_phn values('01','012-3456-7890');
insert into grp_phn values('02','012-3456-7890');
insert into grp_phn values('03','012-3456-7890');
insert into grp_phn values('03','012-3456-7891');
commit;

begin;
delete from emp_grp;
delete from grp_phn;
delete from mst_group;
delete from mst_emp;
rollback;

