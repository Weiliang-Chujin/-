text_list = "" #词法分析结果的总字符串
str_num = 0  #记字符串索引，即词法分析中第几个单词
#需要的first和fllow集
follow_declaration_list_1 = ["if","while","for","read","write","{",";","ID"]
first_statement_list_1 = ["if","while","for","read","write","{",";","ID"]
first_statement = ["if","while","for","read","write","{",";","ID"]
follow_statement_list_1 = ["}"]
follow_if_stat_1 = ["if","while","for","read","write","{",";","ID","}"]
first_bool_expression = ["(","ID","NUM"]
first_arithmetic_expression = ["(","ID","NUM"]
first_assignment_expression = ["ID"]
first_factor = ["(","ID","NUM"]
first_term = ["(","ID","NUM"]
follow_arithmetic_expression_1 = [";",")",">","<","<=",">=","!=","=="]
follow_term_1 = [";",")","+","-","<",">","<=",">=","==","!="]
symbol_table = {'name':[],'address':[],'value':[]}
str_address = 0 #单词地址
labelp = 0 #跳转标号
save_str = ""

#得到当前单词
def get_str():
    global text_list,str_num
    if str_num != len(text_list):
        return text_list[str_num].split(' ')[0]

#得到具体单词
def real_str():
    global text_list, str_num
    if str_num != len(text_list):
        return text_list[str_num].split(' ')[1].strip('\n')

#插入符号表
def name_def(id_str):
    global symbol_table,str_address
    for i in symbol_table['name']:
        if i == id_str:
            print("变量{}重复定义".format(id_str))
            return
    symbol_table.setdefault('name',[]).append(id_str)
    symbol_table.setdefault('address', []).append(str_address)
    symbol_table.setdefault('value', []).append(False)
    str_address = str_address + 1

#查询符号表
def lookup(id_str):
    global  symbol_table
    for i,str in enumerate(symbol_table['name']):
        if str == id_str:
            address = symbol_table['address'][i]
            return address
    print("变量{}未定义".format(id_str))
    return -1

#是否赋初值
def check_value(id_str):
    global symbol_table
    for i,str in enumerate(symbol_table['name']):
        if str == id_str:
            if symbol_table['value'][i] == False:
                print("变量{}没有赋初值".format(id_str))
            else:
                return

#遇到错误报错后停止程序
def error():
    global str_num
    print("第{}个单词后有错误，编译停止!".format(str_num))
    exit()

#根据test语法规则对每个非终结符写函数，对终结符进行判断，遇到ε的判断是否在左非终结符的FOLLO集中
def program():
    global str_num,text_list,save_str
    if get_str() == '{':
        str_num = str_num + 1
        declaration_list()
        statement_list()
        if get_str() == '}':
            save_str = save_str + "STOP\n"
            saves()
            print("中间代码已保存")
            print("语义分析结束！")
        else:
            error()
    else:
        error()

def declaration_list():
    if get_str() == "int":
        declaration_list_1()
    else:
        error()

def declaration_list_1():
    global follow_declaration_list_1
    if get_str() == "int":
        declaration_stat()
        declaration_list_1()
    elif get_str() in follow_declaration_list_1:
        return
    else:
        error()

def declaration_stat():
    global str_num
    if get_str() == "int":
        str_num = str_num + 1
        if get_str() == "ID":
            name_def(real_str())
            str_num = str_num + 1
            if get_str() == ";":
                str_num = str_num + 1
            else:
                error()
        else:
            error()
    else:
        error()

def statement_list():
    global first_statement_list_1
    if get_str() in first_statement_list_1:
        statement_list_1()
    else:
        error()

def statement_list_1():
    global first_statement,follow_statement_list_1
    if get_str() in first_statement:
        statement()
        statement_list_1()
    elif get_str() in follow_statement_list_1:
        return
    else:
        error()

def statement():
    global str_num
    if get_str() == "if":
        if_stat()
    elif get_str() == "while":
        while_stat()
    elif get_str() == "for":
        for_stat()
    elif get_str() == "read":
        read_stat()
    elif get_str() == "write":
        write_stat()
    elif get_str() == "{":
        compound_stat()
    elif get_str() == "ID":
        assignment_stat()
    elif get_str() == ";":
        str_num = str_num + 1
    else:
        error()

def if_stat():
    global str_num,labelp,save_str
    if get_str() == "if":
        str_num = str_num + 1
        if get_str() == "(":
            str_num = str_num + 1
            if get_str() in first_bool_expression:
                bool_expression()
                if get_str() == ")":
                    label1 = labelp
                    labelp = labelp + 1
                    save_str = save_str + "BRF LABEL"+str(label1)+"\n"
                    str_num = str_num + 1
                    if get_str() in first_statement:
                        statement()
                        label2 = labelp
                        labelp = labelp + 1
                        save_str = save_str + "BR LABEL" + str(label2) + "\n"
                        save_str = save_str + "LABEL" + str(label1) + "\n"
                        if get_str() == "else":
                            if_stat_1()
                        else:
                            error()
                        save_str = save_str + "LABEL" + str(label2) + ":\n"
                    else:
                        error()
                else:
                    error()
            else:
                error()
        else:
            error()
    else:
        error()

def if_stat_1():
    global str_num
    if get_str() == "else":
        str_num = str_num + 1
        if get_str() in first_statement:
            statement()
        else:
            error()
    elif get_str() in follow_if_stat_1:
        return
    else:
        error()

def while_stat():
    global str_num,labelp,save_str
    if get_str() == "while":
        label1 = labelp
        labelp = labelp + 1
        save_str = save_str + "LABEL" + str(label1) + ":\n"
        str_num = str_num + 1
        if get_str() == "(":
            str_num = str_num + 1
            if get_str() in first_bool_expression:
                bool_expression()
                if get_str() == ")":
                    label2 = labelp
                    labelp = labelp + 1
                    save_str = save_str + "BRF LABEL" + str(label2) + "\n"
                    str_num = str_num + 1
                    if get_str() in first_statement:
                        statement()
                    else:
                        error()
                    save_str = save_str + "BRF LABEL" + str(label1) + "\n"
                    save_str = save_str + "LABEL" + str(label2) + ":\n"
                else:
                    error()
            else:
                error()
        else:
            error()
    else:
        error()

def for_stat():
    global str_num,labelp,save_str
    if get_str() == "for":
        str_num = str_num + 1
        if get_str() == "(":
            str_num = str_num + 1
            if get_str() in first_assignment_expression:
                assignment_expression()
                if get_str() == ";":
                    label1 = labelp
                    labelp = labelp + 1
                    save_str = save_str + "LABEL" + str(label1) + ":\n"
                    str_num = str_num + 1
                    if get_str() in first_bool_expression:
                        bool_expression()
                        label2 = labelp
                        labelp = labelp + 1
                        save_str = save_str + "BRF LABEL" + str(label2) + "\n"
                        label3 = labelp
                        labelp = labelp + 1
                        save_str = save_str + "BRF LABEL" + str(label3) + "\n"
                        if get_str() == ";":
                            label4 = labelp
                            labelp = labelp + 1
                            save_str = save_str + "LABEL" + str(label4) + ":\n"
                            str_num = str_num + 1
                            if get_str() in first_assignment_expression:
                                assignment_expression()
                                save_str = save_str + "BR LABEL" + str(label1) + "\n"
                                if get_str() == ")":
                                    save_str = save_str + "LABEL" + str(label3) + ":\n"
                                    str_num = str_num + 1
                                    if get_str() in first_statement:
                                        statement()
                                        save_str = save_str + "BR LABEL" + str(label4) + "\n"
                                        save_str = save_str + "LABEL" + str(label2) + ":\n"
                                    else:
                                        error()
                                else:
                                    error()
                            else:
                                error()
                        else:
                            error()
                    else:
                        error()
                else:
                    error()
            else:
                error()
        else:
            error()
    else:
        error()

def read_stat():
    global str_num,save_str
    if get_str() == "read":
        str_num = str_num + 1
        if get_str() == "ID":
            address = lookup(real_str())
            str_num = str_num + 1
            if get_str() == ";":
                if address != -1:
                    symbol_table['value'][address] = True #赋初值
                    save_str = save_str + "IN\n"
                    save_str = save_str + "STO "+str(address)+"\n"
                    save_str = save_str + "POP\n"
                str_num = str_num + 1
            else:
                error()
        else:
            error()
    else:
        error()

def write_stat():
    global str_num,save_str
    if get_str() == "write":
        str_num = str_num + 1
        if get_str() in first_arithmetic_expression:
            arithmetic_expression()
            if get_str() == ";":
                save_str = save_str + "OUT\n"
                str_num = str_num + 1
            else:
                error()
        else:
            error()
    else:
        error()

def compound_stat():
    global str_num
    if get_str() == "{":
        str_num = str_num + 1
        if get_str() in first_statement_list_1:
            statement_list()
            if get_str() == "}":
                str_num = str_num + 1
            else:
                error()
        else:
            error()
    else:
        error()

def assignment_expression():
    global str_num,symbol_table,save_str
    if get_str() == "ID":
        address = lookup(real_str())
        str_num = str_num + 1
        if get_str() == "=":
            str_num = str_num + 1
            if get_str() in first_arithmetic_expression:
                arithmetic_expression()
                if address != -1:
                    symbol_table['value'][address] = True #赋初值
                    save_str = save_str + "STO "+str(address)+"\n"
                    save_str = save_str + "POP\n"
            else:
                error()
        else:
            error()
    else:
        error()

def assignment_stat():
    global str_num
    if get_str() in first_assignment_expression:
        assignment_expression()
        if get_str() == ";":
            str_num = str_num + 1
        else:
            error()
    else:
        error()

def bool_expression():
    if get_str() in first_arithmetic_expression:
        arithmetic_expression()
        bool_expression_1()
    else:
        error()

def bool_expression_1():
    global str_num,save_str
    if get_str() == ">":
        str_num = str_num + 1
        if get_str() in first_arithmetic_expression:
            arithmetic_expression()
            save_str = save_str + "GT\n"
        else:
            error()
    elif get_str() == "<":
        str_num = str_num + 1
        if get_str() in first_arithmetic_expression:
            arithmetic_expression()
            save_str = save_str + "LES\n"
        else:
            error()
    elif get_str() == "<=":
        str_num = str_num + 1
        if get_str() in first_arithmetic_expression:
            arithmetic_expression()
            save_str = save_str + "LE\n"
            print(" LE")
        else:
            error()
    elif get_str() == ">=":
        str_num = str_num + 1
        if get_str() in first_arithmetic_expression:
            arithmetic_expression()
            save_str = save_str + "GE\n"
        else:
            error()
    elif get_str() == "==":
        str_num = str_num + 1
        if get_str() in first_arithmetic_expression:
            arithmetic_expression()
            save_str = save_str + "EQ\n"
        else:
            error()
    elif get_str() == "!=":
        str_num = str_num + 1
        if get_str() in first_arithmetic_expression:
            arithmetic_expression()
            save_str = save_str + "NOTEQ\n"
        else:
            error()
    else:
        error()

def arithmetic_expression():
    if get_str() in first_term:
        term()
        arithmetic_expression_1()
    else:
        error()

def arithmetic_expression_1():
    global str_num,follow_arithmetic_expression_1,save_str
    if get_str() == "+":
        str_num = str_num + 1
        if get_str() in first_term:
            term()
            arithmetic_expression_1()
            save_str = save_str + "ADD\n"
        else:
            error()
    elif get_str() == "-":
        str_num = str_num + 1
        if get_str() in first_term:
            term()
            arithmetic_expression()
            save_str = save_str + "SUB\n"
        else:
            error()
    elif get_str() in follow_arithmetic_expression_1:
        return
    else:
        error()

def term():
    if get_str() in first_factor:
        factor()
        term_1()
    else:
        error()

def term_1():
    global str_num,follow_term_1,save_str
    if get_str() == "*":
        str_num = str_num + 1
        if get_str() in first_factor:
            factor()
            save_str = save_str + "MULT\n"
        else:
            error()
    elif get_str() == "/":
        str_num = str_num + 1
        if get_str() in first_factor:
            factor()
            save_str = save_str + "DIV\n"
        else:
            error()
    elif get_str() in follow_term_1:
        return
    else:
        error()

def factor():
    global str_num,save_str
    if get_str() == "(":
        str_num = str_num + 1
        if get_str() in first_arithmetic_expression:
            arithmetic_expression()
            if get_str() == ")":
                str_num = str_num + 1
            else:
                error()
        else:
            error()
    elif get_str() == "ID":
        address = lookup(real_str())
        if address != -1:
            check_value(real_str())
            save_str = save_str +"LOAD "+str(address) +"\n"
        str_num = str_num + 1
    elif get_str() == "NUM":
        save_str = save_str + "LOADI " + str(real_str()) + "\n"
        str_num = str_num + 1
    else:
        error()

#保存中间代码
def saves():
    global save_str
    save_path = "中间代码.txt"
    fw = open(save_path, 'w')
    fw.writelines(save_str)
    fw.close()

#主函数
if __name__ == '__main__':
    file_path = "lex4.txt"
    text_file = open(file_path, 'r')
    text_list = text_file.readlines()
    print("语义分析开始：")
    program()