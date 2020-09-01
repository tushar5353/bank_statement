create table if not exists <STAGE_DB>.<STAGE_TRANSACTIONS>_temp(
id int not null auto_increment,
row_sha varchar(200),
date_time datetime not null,
description text,
category varchar(20) default null,
info varchar(200) default null,
debit double,
credit double,
balance double not null,
bank_name enum('citibank') not null,
created_at datetime default now(),
updated_at datetime,
primary key (id)
)
