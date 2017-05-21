import compile as cp
import getpass
#import pandas as pd

def read_users():
    file = open("data/users.txt")
    names = []
    passwords = []
    for line in file.readlines():
        line = line.strip().split()
        names.append(line[0])
        passwords.append(line[1])
    return names, passwords

if __name__ == '__main__':
    while True:
        names, passwords = read_users()
        name = input("name:")
        if name not in names:
            print("user %s is not exist!" %name)
            continue

        password = input("password:")
        if password != passwords[names.index(name)]:
            print("user %s's password is wrong!" % name)
            continue
        print("************************************************")
        print("the word or symbol of order are divided by space ")
        print("            input over to exit                   ")
        print("************************************************")
        comp = cp.compile(name)
        while True:
            order = input("SQL>>")
            if len(order) > 2:
                order = order.lower().strip().split()
                if len(order) > 0 and order[0] == "over":
                    break
                if not comp.compile(order):
                    print("wrong order !")



#drop table ss
#create table aty ( ID int . name char )
#insert into aty (values( 23 , aty ))
#select ID from student where a=1
#CREATE USER zrr IDENTIFIED BY 1234567890
#CREATE INDEX aaa ON bbb ( cc , d )
#update www set aaa = bbb , ccc = ddd where eee = fff
#select * from aty
#alter table r add sex int
#alter table r drop name
#update aty set sex = f where id = 34
#delete from aty where id = 34
#alter table class drop name

# 测试index
# create table class ( ID int , name char )
#
# insert into class (values( 0 , nlp ))
# insert into class (values( 1 , math_1 ))
# insert into class (values( 2 , db ))
# insert into class (values( 3 , picture ))
# insert into class (values( 4 , english ))
# insert into class (values( 4 , chinese ))
# insert into class (values( 6 , history ))
# insert into class (values( 8 , japanese ))
# insert into class (values( 8 , world ))
# insert into class (values( 9 , math_2 ))
# insert into class (values( 11 , math_3 ))
# insert into class (values( 14 , c ))
# insert into class (values( 15 , java ))
# insert into class (values( 19 , python ))
#
# create index class_ID on class (ID)
#select * from student,class
#select * from student,class
#select class.id from class
#select class.id,class.name from class,student
#select * from class,student where student.id = 20143958
#select * from class,student where student.id > 20146665
#select * from class,student where student.id > 20146665 and student.id = 20143958
#select * from student where student.id > 20146665 and student.id = 20143958
#select student.name,student.id from student where student.id = 20143958
#select student.name,student.id,class.name from student,class where student.id > 20143958 and class.id = 0
#grant 0100 on student to cy