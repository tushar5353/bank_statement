CREATE TABLE IF NOT EXISTS <MASTER_DB>.<MASTER_TRANSACTIONS>(
id int(11) not null auto_increment,
row_sha varchar(200) default null,
date_time datetime,
description text,
category varchar(20) default null,
info varchar(200) default null,
amount double,
transaction_type enum('credit', 'debit'),
balance double,
bank_name enum('citibank'),
created_at datetime default now(),
updated_at datetime,
primary key(id)
)
