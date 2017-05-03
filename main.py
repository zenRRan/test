import compile as cp
#import pandas as pd

if __name__ == '__main__':
    print("************************************************")
    print("the word or symbol of order are divided by space ")
    print("            input over to exit                   ")
    print("************************************************")
    comp = cp.compile()
    while True:
        # print(pd.read_table("./data/table_classes.txt", ))
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