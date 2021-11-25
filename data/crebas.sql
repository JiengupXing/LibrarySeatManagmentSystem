create database LSMS
on
(name=lsms_data,
filename='e:\lsms_data.mdf' ,
size=10,
maxsize=50,
filegrowth=1)
log on
( name=cap_log, 
filename='e:\lsms_log.ldf ' , 
size=2 , 
maxsize=5 , 
filegrowth=1)
go


use LSMS

go
/*==============================================================*/
/* DBMS name:      Microsoft SQL Server 2005                    */
/* Created on:     2019/12/2 11:25:12                           */
/*==============================================================*/


if exists (select 1
   from sys.sysreferences r join sys.sysobjects o on (o.id = r.constid and o.type = 'F')
   where r.fkeyid = object_id('Seats') and o.name = 'FK_SEATS_BELONG TO_ROOMS')
alter table Seats
   drop constraint "FK_SEATS_BELONG TO_ROOMS"
go

if exists (select 1
   from sys.sysreferences r join sys.sysobjects o on (o.id = r.constid and o.type = 'F')
   where r.fkeyid = object_id('Students') and o.name = 'FK_STUDENTS_STUDY IN_INSTITUT')
alter table Students
   drop constraint "FK_STUDENTS_STUDY IN_INSTITUT"
go

if exists (select 1
            from  sysobjects
           where  id = object_id('Institutes')
            and   type = 'U')
   drop table Institutes
go

if exists (select 1
            from  sysobjects
           where  id = object_id('Librarians')
            and   type = 'U')
   drop table Librarians
go

if exists (select 1
            from  sysindexes
           where  id    = object_id('Records')
            and   name  = 'Recoders2_FK'
            and   indid > 0
            and   indid < 255)
   drop index Records.Recoders2_FK
go

if exists (select 1
            from  sysobjects
           where  id = object_id('Records')
            and   type = 'U')
   drop table Records
go

if exists (select 1
            from  sysobjects
           where  id = object_id('Rooms')
            and   type = 'U')
   drop table Rooms
go

if exists (select 1
            from  sysindexes
           where  id    = object_id('Seats')
            and   name  = 'Belong to_FK'
            and   indid > 0
            and   indid < 255)
   drop index Seats."Belong to_FK"
go

if exists (select 1
            from  sysobjects
           where  id = object_id('Seats')
            and   type = 'U')
   drop table Seats
go

if exists (select 1
            from  sysindexes
           where  id    = object_id('Students')
            and   name  = 'Study in_FK'
            and   indid > 0
            and   indid < 255)
   drop index Students."Study in_FK"
go

if exists (select 1
            from  sysobjects
           where  id = object_id('Students')
            and   type = 'U')
   drop table Students
go

/*==============================================================*/
/* Table: Institutes                                            */
/*==============================================================*/
create table Institutes (
   Iid                  bigint               not null,
   Iname                varchar(100)         not null,
   Ishort               varchar(10)          not null,
   Itotal_stuents       int                  null,
   Itotal_teachers      int                  null,
   constraint PK_INSTITUTES primary key nonclustered (Iid)
)
go

if exists (select 1 from  sys.extended_properties
           where major_id = object_id('Institutes') and minor_id = 0)
begin 
   declare @CurrentUser sysname 
select @CurrentUser = user_name() 
execute sp_dropextendedproperty 'MS_Description',  
   'user', @CurrentUser, 'table', 'Institutes' 
 
end 


select @CurrentUser = user_name() 
execute sp_addextendedproperty 'MS_Description',  
   'The imformation of a institution', 
   'user', @CurrentUser, 'table', 'Institutes'
go

/*==============================================================*/
/* Table: Librarians                                            */
/*==============================================================*/
create table Librarians (
   Uid                  bigint               not null,
   Upasswd              varchar(20)          not null,
   Uname                varchar(10)          not null,
   Usex                 varchar(1)           null,
   Uage                 int                  null,
   Lworkage             int                  null,
   constraint PK_LIBRARIANS primary key nonclustered (Uid)
)
go

if exists (select 1 from  sys.extended_properties
           where major_id = object_id('Librarians') and minor_id = 0)
begin 
   declare @CurrentUser sysname 
select @CurrentUser = user_name() 
execute sp_dropextendedproperty 'MS_Description',  
   'user', @CurrentUser, 'table', 'Librarians' 
 
end 


select @CurrentUser = user_name() 
execute sp_addextendedproperty 'MS_Description',  
   'It contains the information of Librarian.', 
   'user', @CurrentUser, 'table', 'Librarians'
go

/*==============================================================*/
/* Table: Records                                               */
/*==============================================================*/
create table Records (
   RCDid                varchar(10)          not null,
   Uid                  bigint               not null,
   Rid                  varchar(10)          not null,
   STid                 varchar(10)          not null,
   Rtime                datetime             not null,
   Roperator_type       varchar(10)          null,
   Roperation           varchar(10)          null,
   constraint PK_RECORDS primary key nonclustered (RCDid, Uid)
)
go

if exists (select 1 from  sys.extended_properties
           where major_id = object_id('Records') and minor_id = 0)
begin 
   declare @CurrentUser sysname 
select @CurrentUser = user_name() 
execute sp_dropextendedproperty 'MS_Description',  
   'user', @CurrentUser, 'table', 'Records' 
 
end 


select @CurrentUser = user_name() 
execute sp_addextendedproperty 'MS_Description',  
   'It indicates the relationship between Users and Seat.', 
   'user', @CurrentUser, 'table', 'Records'
go

/*==============================================================*/
/* Index: Recoders2_FK                                          */
/*==============================================================*/
create index Recoders2_FK on Records (
Rid ASC,
STid ASC
)
go

/*==============================================================*/
/* Table: Rooms                                                 */
/*==============================================================*/
create table Rooms (
   Rid                  varchar(10)          not null,
   Rfloor               int                  null,
   constraint PK_ROOMS primary key nonclustered (Rid)
)
go

if exists (select 1 from  sys.extended_properties
           where major_id = object_id('Rooms') and minor_id = 0)
begin 
   declare @CurrentUser sysname 
select @CurrentUser = user_name() 
execute sp_dropextendedproperty 'MS_Description',  
   'user', @CurrentUser, 'table', 'Rooms' 
 
end 


select @CurrentUser = user_name() 
execute sp_addextendedproperty 'MS_Description',  
   'It contains the location information of room.', 
   'user', @CurrentUser, 'table', 'Rooms'
go

/*==============================================================*/
/* Table: Seats                                                 */
/*==============================================================*/
create table Seats (
   Rid                  varchar(10)          not null,
   STid                 varchar(10)          not null,
   STtype               varchar(10)          not null,
   STstatus             bit                  not null,
   constraint PK_SEATS primary key nonclustered (Rid, STid)
)
go

if exists (select 1 from  sys.extended_properties
           where major_id = object_id('Seats') and minor_id = 0)
begin 
   declare @CurrentUser sysname 
select @CurrentUser = user_name() 
execute sp_dropextendedproperty 'MS_Description',  
   'user', @CurrentUser, 'table', 'Seats' 
 
end 


select @CurrentUser = user_name() 
execute sp_addextendedproperty 'MS_Description',  
   'It contains whether a seat is empty or not.', 
   'user', @CurrentUser, 'table', 'Seats'
go

/*==============================================================*/
/* Index: "Belong to_FK"                                        */
/*==============================================================*/
create index "Belong to_FK" on Seats (
Rid ASC
)
go

/*==============================================================*/
/* Table: Students                                              */
/*==============================================================*/
create table Students (
   Uid                  bigint               not null,
   Upasswd              varchar(20)          not null,
   Uname                varchar(10)          not null,
   Usex                 varchar(1)           null,
   Uage                 int                  null,
   Iid                  bigint               not null,
   Sclass               varchar(10)          not null,
   Smajor               varchar(10)          null,
   Sinstitute           varchar(10)          not null,
   constraint PK_STUDENTS primary key nonclustered (Uid)
)
go

if exists (select 1 from  sys.extended_properties
           where major_id = object_id('Students') and minor_id = 0)
begin 
   declare @CurrentUser sysname 
select @CurrentUser = user_name() 
execute sp_dropextendedproperty 'MS_Description',  
   'user', @CurrentUser, 'table', 'Students' 
 
end 


select @CurrentUser = user_name() 
execute sp_addextendedproperty 'MS_Description',  
   'It contain the imformation of a student.', 
   'user', @CurrentUser, 'table', 'Students'
go

/*==============================================================*/
/* Index: "Study in_FK"                                         */
/*==============================================================*/
create index "Study in_FK" on Students (
Iid ASC
)
go

alter table Seats
   add constraint "FK_SEATS_BELONG TO_ROOMS" foreign key (Rid)
      references Rooms (Rid)
go

alter table Students
   add constraint "FK_STUDENTS_STUDY IN_INSTITUT" foreign key (Iid)
      references Institutes (Iid)
go

