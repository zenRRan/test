'''
created by zenRRan 2017.4.18
'''

import os
import re

'''functions'''
'''
def __init__(self)
def select(self, str)
def insert(self, str)
def alert_table(self, str)
def read_file(self)
def compile(self, str)
def create_file(self, file_name)
def insert2file(self, str, dir)
def delete_file(self, file_name)
def drop_table(self, str)
def create_table(self, str)
def delete_from_where(self, str)
def update_set(self, str)
def create_index_on(self, str)
def drop_index(self, str)
def grant_on_to(self, str)
def remove_on_from(self, str)
def create_user(self, str)
def read_user(self)
def read_table(self, filename)
'''
class compile(object):

    def __init__(self):
        self.class_file_path = "./data/table_classes.txt"
        self.class_index_file = "./data/tables_index.txt"
        self.table_path = "./data/table/"
        self.index_path = "./data/index/"
        self.data_path = "./data/"
        self.file_type = ".txt"

        self.read_file()
        self.flag = False

    def compile(self, str):
        if self.create_table(str):
            return True
        elif self.drop_table(str):
            return True
        elif self.insert(str):
            return True
        elif self.select(str):
            return True
        elif self.create_user(str):
            return True
        elif self.alter_table(str):
            return True
        elif self.remove_on_from(str):
            return True
        elif self.grant_on_to(str):
            return True
        elif self.create_index_on(str):
            return True
        elif self.drop_index(str):
            return True
        elif self.update_set(str):
            return True
        elif self.delete_from_where(str):
            return True
        else:
            return False

    '''
    （5）DELETE FROM 关系名
     [WHERE条件表达式] //条件表达式包括and、or、=、≠、≤、≥、<、>
    '''
    def delete_from_where(self, str):
        self.read_file()
        pattern = re.compile(r'\s*delete\s+from\s+\S+\s+where\s+\S+\s*=\s*\S+\s*')
        sent = " ".join(str)
        match = pattern.match(sent)
        if match and match.group() == sent:
            if str[2] not in self.table_names:
                print("%s is not in tables!" % str[2])
                return True
            where_str = sent[sent.index("where")+5:]
            where_list = "".join(where_str.strip().split()).split("=")
            where_left = where_list[0]
            where_right = where_list[1]
            if where_left not in self.table_dic[str[2]]:
                print("%s is not in table %s!" %(where_left, str[2]))
                return True
            index = self.table_names.index(str[2])
            pros = self.property_type[index][::2]
            # types = self.property_type[index][1::2]
            index_where = pros.index(where_left)
            table_lines = self.read_table(str[2])
            k = 0
            flag = False
            for k in range(len(table_lines)):
                if table_lines[k].strip().split()[index_where] == where_right:
                    flag = True
                    break
            if flag:
                del table_lines[k]
                print("delete from %s where %s = %s succeed!" % (str[2], where_left, where_right))
                file = open(self.table_path + str[2] + self.file_type, "w")
                for i in range(len(table_lines)):
                    file.write(table_lines[i] + '\n')
                file.close()
                #-----------index---------------------
                self.refresh_index_file(str[2],where_left)
                # ------------------------------------
                return True
        return False
    '''
    （6）UPDATE 关系名
     SET 〈列名〉=〈常值〉，…，〈列名〉=〈常值〉
     [WHERE 条件表达式]  //同delete

     update aty set sex = m where id = 25
    '''
    def update_set(self, str):
        self.read_file()
        pattern = re.compile(r"update\s+\S+\s+set\s+\S+\s*=\s*\S+\s*(\s*,\s*\S+\s*=\s*\S+\s*)*where\s+\S+\s*=\s*\S+\s*")
        sent = " ".join(str)
        match = pattern.match(sent)
        if match and match.group() == sent:
            # print(str[1], self.table_names)
            if str[1] not in self.table_names:
                print("%s is not in tables!" % str[1])
                return True
            where_str = sent[sent.index("where")+5:]
            where_list = "".join(where_str.strip().split()).split("=")
            where_left = where_list[0]
            where_right = where_list[1]
            if where_left not in self.table_dic[str[1]]:
                print("%s is not in table %s!" %(where_left, str[1]))
                return True
            index = self.table_names.index(str[1])
            pros = self.property_type[index][::2]
            types = self.property_type[index][1::2]
            set_str = sent[sent.index("set")+3:sent.index("where")]
            op_list = "".join(set_str.strip().split()).split(",")
            op_left = []
            op_right = []
            for op in op_list:
                o = op.split("=")
                op_left.append(o[0])
                op_right.append(o[1])

            index_where = pros.index(where_left)
            table_lines = self.read_table(str[1])
            k = 0
            flag = False
            for k in range(len(table_lines)):
                if table_lines[k].strip().split()[index_where] == where_right:
                    flag = True
                    break
            if flag:
                table_list = table_lines[k].split()
                for i in range(len(op_left)):
                    index = pros.index(op_left[i])
                    table_list[index] = op_right[i]
                table_lines[k] = " ".join(table_list)
                file = open(self.table_path + str[1] + self.file_type, "w")
                for i in range(len(table_lines)):
                    file.write(table_lines[i]+'\n')
                file.close()
                for op in op_left:
                    # -----------index---------------------
                    self.refresh_index_file(str[1], op)
                    # ------------------------------------
                print("update succeed!")
                return True
            else:
                print("no %s in the table's %s!" %(where_right, where_left))

        return False

    '''
    （8）CREATE INDEX 索引名 ON 关系名 (属性名,......,属性名)
     create index class_ID on class (ID)
    '''
    def create_index_on(self, str):
        self.read_file()
        pattern = re.compile(r"create\s+index\s+\S+\s+on\s+\S+\s*\(\s*\S+(\s*,\s*\S+\s*)*\)")
        sent = " ".join(str)
        match = pattern.match(sent)
        if match and match.group() == sent:
            # print(str[4], " ", self.table_names)
            if str[4] not in self.table_names:
                print("%s is not in tables !" %str[4])
                return True
            begin = sent.index("(")
            end = sent.index(")")
            ppts = sent[begin+1:end].split(",")
            for pro in ppts:
                if pro not in self.table_dic[str[4]]:
                    print("%s is not in %s's properties!" %(pro, str[4]))
                    return True
            for pro in ppts:
                self.write2indexfile(self.class_index_file,str[4], pro)
                proIndex = self.table_dic[str[4]][::2].index(pro)
                # print("proIndex=", proIndex)
                # print("dic %s is " %(str[4],))
                type = self.table_dic[str[4]][1::2][proIndex]
                # print("type", type)
                tablelines = self.read_table(str[4])
                #判断是否有序
                flag = True
                buffer = []
                if type == "int":
                    for line in tablelines:
                        buffer.append(int(line.split()[proIndex]))
                else:
                    for line in tablelines:
                        buffer.append(line.split()[proIndex])
                isfirst = True
                bigger = True
                smaller = True
                if len(buffer) > 0:
                    for i in buffer:
                        if isfirst == True:
                            first = i
                            isfirst = False
                        elif i > first:
                            first = i
                            if smaller:
                                bigger = False
                            else:
                                flag = False
                                break
                        elif i == first:
                            continue
                        else:
                            first = i
                            if bigger:
                                smaller = False
                            else:
                                flag = False
                                break
                if flag:
                    step = 4
                    indexData0 = buffer[::step+1]
                    indexData1 = [i*(step+1) for i in range(len(indexData0))]
                    file = open(self.index_path+str[2]+self.file_type,'w')
                    for i in range(len(indexData0)):
                        file.write(self.int2str(indexData0[i])+" "+self.int2str(indexData1[i])+'\n')
                    print("create index %s on %s's %s succeed!" %(str[2],str[4],pro))
                else:
                    indexData = sorted(list(zip(buffer, list(range(len(buffer))))))
                    file = open(self.index_path + str[2]+self.file_type, 'w')
                    for i in range(len(indexData)):
                        file.write(self.int2str(indexData[i][0]) + " " + self.int2str(indexData[i][1])+"\n")
                    print("create index %s on %s's %s succeed!" % (str[2], str[4], pro))
            return True
        else:
            return False

    def int2str(self,s):
        return str(s)
    def readIndexFile(self):
        file = open(self.class_index_file)
        buffer = []
        for line in file.readlines():
            buffer.append(line.strip().split())
        file.close()
        return buffer
    def write2indexfile(self,filepath,clas,pro):
        classes =[e[0] for e in self.readIndexFile()]
        pros = [e[1:] for e in self.readIndexFile()]
        if clas in classes:
            class_ps = pros[classes.index(clas)]
            if pro in class_ps:
                return
            else:
                class_ps.append(pro)
        else:
            classes.append(clas)
            pros.append([pro])
        file = open(filepath, "w")
        for i in range(len(classes)):
            file.write(classes[i]+" "+" ".join(pros[i])+"\n")
        file.close()
        # print("write to indexfile succeed!")

    def refresh_index_file(self,str,pro):
        if str in self.index_classes and pro in self.index_properties[self.index_classes.index(str)]:
            index_order = "create index " + str + "_" + pro + " on " + str + " (" + pro + ")"
            index_order = index_order.strip().split()
            self.create_index_on(index_order)
            print("index %s_%s have been refreshed!" % (str, pro))

    '''
    （9）DROP INDEX 索引名
    '''
    def drop_index(self, str):
        if len(str) == 3 and str[0] == "drop" and str[1] == "index":
            lines = self.readIndexFile()
            clas = str[2].split("_")[0]
            pro = str[2].split("_")[1]
            classes = [line[0] for line in lines]
            pros = [line[1:] for line in lines]
            path = self.index_path+str[2]+self.file_type
            if os.path.isfile(path):
                if pro in pros[classes.index(clas)]:
                    pros[classes.index(clas)].remove(pro)
                    with open(self.class_index_file, "w") as file:
                        for i in range(len(classes)):
                            file.write(classes[i] + " " + " ".join(pros[i]) + "\n")
                    os.remove(path)
                    print("drop index %s succeed!" % str[2])
                    return True
                else:
                    print("%s is not exist!" % pro)
            else:
                print("%s is not exist!" %str[2])



        else:
            return False





    '''
    （13）GRANT 权限列表  //自己实现的所有SQL命令
     ON 关系名
     TO 用户列表
    '''
    def grant_on_to(self, str):
        if len(str) == 6 and str[0] == "grant" and str[2] == "on" and str[4] == "to":
            print("grant ... on ... to ... ")
            return True
        else:
            return False

    '''
    （14）REVOKE 权限列表  //同GRANT
     ON 关系名
     FROM 用户列表
    '''
    def remove_on_from(self, str):
        if len(str) == 6 and str[0] == "remove" and str[2] == "on" and str[4] == "from":
            print("remove ... on ...from ... ")
            return True
        else:
            return False


    '''
    （12）CREATE USER 用户名 IDENTIFIED BY 密码
    '''
    def create_user(self, str):
        if str[0] == "create" and str[1] == "user" and str[3] == "identified" and str[4] == "by" and len(str) == 6:
            path = self.data_path+"users"+self.file_type
            if not os.path.isfile(path):
                file = open(path, "w")
                file.close()
            self.read_user()
            file = open(path, "a+")
            if str[2] in self.username:
                print("user name is have been applyed!")
                file.close()
                return True
            file.write(str[2]+" "+str[5])
            file.close()
            print("create user right!")
            return True
        else:
            return False

    '''
    read user table
    '''
    def read_user(self):
        path = self.data_path + "users" + self.file_type
        file = open(path)
        self.username = []
        self.password = []
        for line in file.readlines():
            l = line.strip().split()
            self.username.append(l[0])
            self.password.append(l[1])
        file.close()

    '''
    read table
    '''
    def read_table(self, filename):
        path = self.table_path+filename+self.file_type
        buffer = []
        if os.path.isfile(path):
            file = open(path)
            for line in file.readlines():
                buffer.append(line.strip())
            return buffer
        return None
    '''
    （7）SELECT *|属性名列表
     FROM 关系名列表
     WHERE 条件表达式 //同delete
    '''
    def select(self, str):
        self.read_file()
        sent = " ".join(str)
        pattern0 = re.compile(r'select(\s+\*\s+)from(\s\S+\s)*(where)?(\s\S+\s*)')
        match0 = pattern0.match(sent)
        #select * from ... where ...
        if match0 and match0.group() == sent:
            from_end = sent.find("from")+4
            where_begin = sent.find("where")
            if where_begin < 0:
                cur_str = "".join(str[3:]).split(",")
                tables = []
                for table in cur_str:
                    if table in self.table_names:
                        tables.append(table)
                    else:
                        print("%s is not in the table!" % table)
                        return True
                for table in tables:
                    print("__________________________________________________________________________________")
                    print("table name ", table)
                    pro = self.table_dic[table][::2]
                    for p in pro:
                        print("%-15s" %p, end="")
                    print()
                    lines = self.read_table(table)
                    if lines != None:
                        for line in lines:
                            l = line.split()
                            for p in l:
                                print("%-15s" % p, end="")
                            print()
                    else:
                        print("%s is not opened!" % table)
                return True


            else:
                if from_end > 0 and where_begin > 0:
                    tables = sent[from_end:where_begin]
                    tables = tables.strip().split(",")
                    datas = []
                    for index in range(len(tables)):
                        tables[index] = tables[index].strip()
                        if tables[index] not in self.table_names:
                            print("%s is not in the tables !" % tables[index])
                        datas.append(self.read_table(tables[index]))
                    data_dic = dict(zip(tables, datas))
        return False

    def select_from_index(self, table, pro, data):
        indexFilelines = self.readIndexFile()
        tables = [line[0] for line in indexFilelines]
        pros = [line[1:] for line in indexFilelines]
        if table not in tables and pro not in pros[tables.index(table)]:
            return None
        output = []

    def Cartesian_product(self, table1, table2=[]):
        buffer = []
        if table2 != []:
            for line1 in table1:
                for line2 in table2:
                    buffer.append(line1.strip() + " " + line2.strip())
        else:
            buffer = " ".join(table1)
        return buffer



    '''
    （4）INSERT INTO 关系名 [(<列名>, …,<列名>)]
     (VALUES(<常值>,...,<常值>))
    '''
    def insert(self, str):
        self.read_file()
        if str[0] == "insert" and str[1] == "into":
            if str[2] in self.table_names:
                if str[3] == "(values(":
                    if str[-1] == "))":
                        values = str[4:-1]
                        dic = self.table_dic[str[2]]
                        pros = [dic[i] for i in range(0, len(dic), 2)]
                        dic = [dic[i] for i in range(1, len(dic), 2)]
                        length = len(dic)
                        if length != 1:
                            length = length*2 - 1
                        if len(values) == length:
                            values = "".join(values).split(",")
                            output = []
                            for i in range(len(values)):
                                if dic[i] == "int" :
                                   if values[i].isdigit():
                                        output.append(values[i])
                                   else:
                                       print("type is int, but %s is not !" % values[i])
                                       return True
                                else:
                                    output.append(values[i])

                            # output = "\n" + " ".join(output)
                            output = " ".join(output)+"\n"
                            self.insert2file(output, self.table_path+str[2]+self.file_type)
                            for pro in pros:
                                # --------------index--------------------------
                                self.refresh_index_file(str[2], pro)
                                # ---------------------------------------------
                            print("insert succeed!")

                            return True
                        else:
                            print("length is not suit !")
                            return True
                    else:
                        print("no '))' !")
                        return True
                else:
                    print("no '(values(' !")
                    return True
            else:
                print("%s is not in tables !" % str[2])


    '''
    （3）ALTER TABLE 关系名 ADD 属性名 类型
     //支持的类型同create table语句
     ALTER TABLE 关系名 DROP 属性名,……,属性名

     alter table r add sex int
    '''

    def alter_table(self, str):
        self.read_file()
        sent = " ".join(str)
        partern_add = re.compile(r'alter\s+table\s+\S+\s+add\s+\S+\s+\S+\s*')
        partern_drop = re.compile(r'alter\s+table\s+\S+\s+drop\s+\S+\s*(,\s*\S+\s*)*')
        match_add = partern_add.match(sent)
        match_drop = partern_drop.match(sent)
        if match_add and match_add.group() == sent:
            table = str[2]
            pro = str[4]
            pro_type = str[5]
            if pro not in self.table_dic[table]:
                index = self.table_names.index(table)
                self.tables[index] = self.tables[index] + " "+pro + " "+pro_type
                file = open(self.class_file_path, "w")
                for line in self.tables:
                    file.write(line+'\n')
                file.close()
                ##################

                ##################
                print("alter add succeed!")
                return True
            else:
                print("%s has been in %s!" % (pro, table))
        elif match_drop and match_drop.group() == sent:
            table = str[2]
            sent = str[4:]
            sent_list = "".join(sent).strip().split(",")
            pros = sent_list[::2]
            for pro in pros:
                if pro not in self.table_dic[table]:
                    print("%s is in table %s" % (pro, table))
                    return True
            table_index = self.table_names.index(table)
            table_list = self.tables[table_index].strip().split()
            for pro in pros:
                pro_index = table_list.index(pro)
                ##########
                tablelines = self.read_table(table)
                lists = []
                for line in tablelines:
                    lists.append(line.split())
                for i in range(len(tablelines)):
                    if len(lists[i]) > pro_index//2:
                        del lists[i][pro_index//2]
                tablefile = open(self.table_path+str[2]+self.file_type,"w")
                for line in lists:
                    tablefile.write(line+"\n")
                ##########
                del table_list[pro_index]
                del table_list[pro_index]

            self.tables[table_index] = " ".join(table_list)
            file = open(self.class_file_path, "w")
            for line in self.tables:
                file.write(line + '\n')
            file.close()

            print("alter drop succeed!")
            return True
        else:
            return False



    '''
    读入数据
    '''
    def read_file(self):
        file = open(self.class_file_path)
        readlines = file.readlines()
        if len(readlines) != 0:
            self.tables = [line.strip() for line in readlines]
            self.table_names = [line.split()[0] for line in self.tables]
            self.property_type = [line.split()[1:] for line in self.tables]
            self.table_dic = dict(zip(self.table_names, self.property_type))
        else:
            self.tables = []
            self.table_names = []
            self.property_type = []
            self.table_dic = []
        file.close()

        file = open(self.class_index_file)
        readlines = file.readlines()
        if len(readlines) != 0:
            self.index_classes = [line.strip().split()[0] for line in readlines]
            self.index_properties = [line.strip().split()[1:] for line in readlines]
            pass
        else:
            self.index_classes = []
            self.index_properties = []
        file.close()


    '''
    创建文件
    '''
    def create_file(self, file_name):
        try:
            file = open(file_name, "w")
            file.close()
        finally:
            pass

    def insert2file(self, str, dir):
        file = open(dir,"a+")
        if file.write(str):
            file.close()
            return True
        file.close()
        print("insert to file failed !")
        return False



    '''
    删除文件
    '''
    def delete_file(self, file_name):
        path = self.table_path+file_name+self.file_type
        if os.path.isfile(path):
            try:
                os.remove(path)
            except:
                print("remove file %s failed !" % file_name)


    '''
    DROP TABLE 关系名
    '''
    def drop_table(self, str):
        self.read_file()
        if len(str) == 3 and str[0] == "drop" and str[1] == "table":
            self.read_file()
            # print(str[2], self.table_names)
            if str[2] not in self.table_names:
                print("%s is not in tables !" %str[2])
                return False
            for index in range(len(self.table_names)):
                if self.table_names[index] == str[2]:
                    break
            del self.tables[index]
            file = open(self.class_file_path,"w")
            file.write("\n".join(self.tables))
            # print(str[2])
            self.delete_file(str[2])
            file.close()
            print("drop table succeed !")
        else:
            return False
        return True


    '''
    CREATE TABLE 关系名
    (属性名 类型,   //类型至少支持int、char两种类型
    属性名 类型)
    '''
    def create_table(self, str):
        self.read_file()
        if str[0] == "create" and str[1] == "table":
            if str[3] == "(":
                if str[-1] == ")":
                    if str[2] in self.table_names:
                        print("%s has been created !" % str[2])
                        return True
                    s = str[4:-1]
                    if len(s) > 2 and len(s) % 2 != 1:
                        print("the form of 'property and type' is wrong !")
                        return True
                    i = 0
                    property = []
                    add_list = [str[2]]
                    file = open(self.class_file_path, 'a+')
                    while i < len(s):
                        if s[i] in property:
                            print("property %s repeat!" % str[i])
                            return True
                        if not (s[i + 1] == 'int' or s[i + 1] == 'char'):
                            print("type %s is wrong!" % s[i + 1])
                            return True
                        add_list.append(s[i])
                        add_list.append(s[i + 1])
                        i = i + 3
                    self.create_file(self.table_path + str[2] + self.file_type)
                    if not self.flag:
                        file.write(" ".join(add_list))
                        self.flag = True
                    else:
                        file.write('\n'+" ".join(add_list))
                    # self.clean(self.table_path + str[2] + self.file_type)
                    print("create %s succeed !" % str[2])
                    file.close()
                    return True
                else:
                    print("no ')' !")
                    return True
            else:
                print("no '(' ！")
                return True
        else:
            return False
        return True

    def clean(self, filepath):
        file = open(filepath,"a+")
        readlines = file.readlines()
        file.close()
        i = 0
        flag = False
        for i in range(len(readlines)):
            if readlines[i] == "" or readlines[i] == "\n" or readlines[i] == " ":
                flag = True
                break
        if flag:
            readlines.remove(i)
            file = open(filepath,"w")
            for i in range(len(readlines)):
                if i == 0:
                    file.write(readlines)

        print(file.readlines())
        file.close()























































