reserved_word = ["if", "else", "for", "while", "int", "read", "write"] #保留字
delimiter = ['(', ')', ';', '{', '}'] #分界符
compare = ['>','<','='] #比较符
operation = ['+','-','*'] #运算符
save_str = "" #待保存字符串
save_text = "" #保存合法单词
errors = 0 #记录错误个数

def Lexical_Analysis(text_str): #词法分析函数
    global reserved_word,delimiter,compare,operation,line_num,save_str,save_text,errors
    status = 0 #状态，0是初态
    line_num = 1 #行数
    for ch in text_str:
        if ch == '\n':
            line_num = line_num + 1
            continue
        status = get_status(ch,status)
        if status == -1: #非法字符错误
            errors = errors+1
            print("第{}行错误：存在非法字符{}".format(line_num, ch))
            status = 0
        elif status == 3 or status == 4 or status == 6 or status == 11:
            save_str = ""
            status = 0
    if status == 9 or status == 10:
        errors = errors + 1
        print("第{}行注释不完整".format(line_num))
    save_this(save_text)
    print("词法分析结束，共发现{}处错误".format(errors))

def get_status(str,sta): #对读入字符，进行状态转换
    global reserved_word, delimiter, compare, operation, line_num,save_str,save_text,errors
    if str == ' ':  #遇到空格
        if sta == 9 or sta == 0:
            return sta
    if sta == 0: #当前状态是初态
        if str.isalpha():
            save_str = save_str + str
            return 1 #标识符状态
        elif str.isdigit() and str != '0':
            save_str = save_str + str
            return 2 #除0外的数字状态
        elif str == '0':
            save_text = save_text + "NUM 0\n"
            return 3 #数字0的状态
        elif str in delimiter:
            save_text = save_text +str+" "+ str+"\n"
            return 4 #分界符的状态
        elif str in compare:
            save_str = save_str + str
            return 5 #比较符的状态
        elif str == '!':
            return 7 #感叹号到!=的状态
        elif str in operation:
            save_text = save_text + str+" "+ str + "\n"
            return 6 #运算符的状态
        elif str == '/':
            return 8 #注释下的状态
        else:
            return -1
    elif sta == 1:
        if str.isalpha() or str.isdigit():
            save_str = save_str + str
            return 1
        else:
            if save_str != "":
                if save_str in reserved_word:
                    save_text = save_text + save_str+" " + save_str + "\n"
                else:
                    save_text = save_text + "ID" + " " + save_str + "\n"
            save_str = ""
            return get_status(str,0)
    elif sta == 2:
        if str.isdigit():
            save_str = save_str + str
            return 2
        else:
            save_text = save_text + "NUM "+save_str+"\n"
            save_str = ""
            return get_status(str, 0)
    elif sta == 5:
        if str == '=':
            save_str = save_str + str
            save_text = save_text + save_str+" "+ save_str + "\n"
            return 6
        else:
            save_text = save_text + save_str + " " + save_str + "\n"
            save_str = ""
            return get_status(str, 0)
    elif sta == 7:
        if str == '=':
            save_text = save_text + "!=" + " " + "!=" + "\n"
            return 6
        else:
            errors = errors+1
            print("第{}行错误：不存在该运算符‘!’".format(line_num))
            return get_status(str, 0)
    elif sta == 8:
        if str == '*':
            return 9
        else:
            return get_status(str, 0)
    elif sta == 9:
        if str == '*':
            return 10
        else:
            return 9
    elif sta == 10:
        if str == '*':
            return 10
        elif str == '/':
            return 11
        else:
            return 9
    else:
        return -1

def save_this(str): #将合法单词写入
    save_path = "lex4.txt"
    fw = open(save_path, 'w')
    fw.writelines(str)
    fw.close()

if __name__ == '__main__': #主函数
    file_path = "text4.txt"
    text_file = open(file_path,'r')
    text_str = ""
    for line in text_file.readlines():
        text_str = text_str + line
    print("词法分析开始：")
    Lexical_Analysis(text_str)
    text_file.close()