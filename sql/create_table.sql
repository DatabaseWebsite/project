use main;

Create table people
(pid int not null unique,
Sname char(20) not null,
username char(50) not null,
password char(50) not null,
email char(50),
ptype int not null,
Primary key(pid)
);


CREATE TABLE permission (
pid int not null unique,
read_permission int,
write_permission int,
Primary key(pid),
Foreign key(pid) references people(pid)
);

CREATE TABLE normal_homework (
hid int not null unique,
start_time char(14),
end_time char(14),
content char(255),
Primary key(hid)
);

CREATE TABLE normal_homework_submit (
hid int not null,
pid int not null,
grade int not null,
submit_time char(14),

Primary key(hid,pid),
FOREIGN KEY (hid) references normal_homework(hid),
FOREIGN KEY (pid) references people(pid),
CHECK ( grade >= 0 and grade <= 100 )
);

CREATE TABLE wiki (
wid int not null unique,
is_stared int,
Primary key(wid)
);

CREATE TABLE reply (
wid int not null unique,
reply_order int not null unique,
pid int not null,
time char(14) not null,
replied_order int,
content char(255),
like_num int,
Primary key(wid,reply_order),
FOREIGN KEY (wid) references wiki(wid),
FOREIGN KEY (pid) references people(pid),
CHECK ( reply_order > reply.replied_order ),
CHECK ( like_num > 0 )
);

CREATE TABLE message (
mid int not null unique,
sender int not null,
receiver int not null,
content char(255) not null,

Primary key(mid),
FOREIGN KEY (sender) references people(pid),
FOREIGN KEY (receiver) references people(pid),
CHECK (not sender = receiver)

);

CREATE TABLE announcement (
aid int not null unique,
sender int not null,
content char(255) not null,

Primary key(aid)
);
