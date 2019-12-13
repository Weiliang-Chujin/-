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

#得到当前单词
def get_str():
    global text_list,str_num
    if str_num != len(text_list):
        return text_list[str_num].split(' ')[0]

#遇到错误报错后停止程序
def error():
    global str_num
    print("第{}个单词后有错误，编译停止!".format(str_num))
    exit()

#根据test语法规则对每个非终结符写函数，对终结符进行判断，遇到ε的判断是否在左非终结符的FOLLO集中
def program():
    global str_num,text_list
    if get_str() == '{':
        str_num = str_num + 1
        declaration_list()
        statement_list()
        if get_str() == '}':
            print("没有语法错误了，语法分析结束！")
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
    global str_num
    if get_str() == "if":
        str_num = str_num + 1
        if get_str() == "(":
            str_num = str_num + 1
            if get_str() in first_bool_expression:
                bool_expression()
                if get_str() == ")":
                    str_num = str_num + 1
                    if get_str() in first_statement:
                        statement()
                        if get_str() == "else":
                            if_stat_1()
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
    global str_num
    if get_str() == "while":
        str_num = str_num + 1
        if get_str() == "(":
            str_num = str_num + 1
            if get_str() in first_bool_expression:
                bool_expression()
                if get_str() == ")":
                    str_num = str_num + 1
                    if get_str() in first_statement:
                        statement()
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

def for_stat():
    global str_num
    if get_str() == "for":
        str_num = str_num + 1
        if get_str() == "(":
            str_num = str_num + 1
            if get_str() in first_assignment_expression:
                assignment_expression()
                if get_str() == ";":
                    str_num = str_num + 1
                    if get_str() in first_bool_expression:
                        bool_expression()
                        if get_str() == ";":
                            str_num = str_num + 1
                            if get_str() in first_assignment_expression:
                                assignment_expression()
                                if get_str() == ")":
                                    str_num = str_num + 1
                                    if get_str() in first_statement:
                                        statement()
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
    global str_num
    if get_str() == "read":
        str_num = str_num + 1
        if get_str() == "ID":
            str_num = str_num + 1
            if get_str() == ";":
                str_num = str_num + 1
            else:
                error()
        else:
            error()
    else:
        error()

def write_stat():
    global str_num
    if get_str() == "write":
        str_num = str_num + 1
        if get_str() in first_arithmetic_expression:
            arithmetic_expression()
            if get_str() == ";":
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
    global str_num
    if get_str() == "ID":
        str_num = str_num + 1
        if get_str() == "=":
            str_num = str_num + 1
            if get_str() in first_arithmetic_expression:
                arithmetic_expression()
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
    global str_num
    if get_str() == ">":
        str_num = str_num + 1
        if get_str() in first_arithmetic_expression:
            arithmetic_expression()
        else:
            error()
    elif get_str() == "<":
        str_num = str_num + 1
        if get_str() in first_arithmetic_expression:
            arithmetic_expression()
        else:
            error()
    elif get_str() == "<=":
        str_num = str_num + 1
        if get_str() in first_arithmetic_expression:
            arithmetic_expression()
        else:
            error()
    elif get_str() == ">=":
        str_num = str_num + 1
        if get_str() in first_arithmetic_expression:
            arithmetic_expression()
        else:
            error()
    elif get_str() == "==":
        str_num = str_num + 1
        if get_str() in first_arithmetic_expression:
            arithmetic_expression()
        else:
            error()
    elif get_str() == "!=":
        str_num = str_num + 1
        if get_str() in first_arithmetic_expression:
            arithmetic_expression()
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
    global str_num,follow_arithmetic_expression_1
    if get_str() == "+":
        str_num = str_num + 1
        if get_str() in first_term:
            term()
            arithmetic_expression_1()
        else:
            error()
    elif get_str() == "-":
        str_num = str_num + 1
        if get_str() in first_term:
            term()
            arithmetic_expression()
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
    global str_num,follow_term_1
    if get_str() == "*":
        str_num = str_num + 1
        if get_str() in first_factor:
            factor()
        else:
            error()
    elif get_str() == "/":
        str_num = str_num + 1
        if get_str() in first_factor:
            factor()
        else:
            error()
    elif get_str() in follow_term_1:
        return
    else:
        error()

def factor():
    global str_num
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
        str_num = str_num + 1
    elif get_str() == "NUM":
        str_num = str_num + 1
    else:
        error()

#主函数
if __name__ == '__main__':
    file_path = "lex2.txt"
    text_file = open(file_path, 'r')
    text_list = text_file.readlines()
    print("语法分析开始：")
    program()