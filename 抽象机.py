#定义一个栈
class ArrayStack:
    def __init__(self):
        # create an empty stack
        self._data=[]
    def __len__(self):
        return len(self._data)
    def is_empty(self):
        return len(self._data)==0
    def push (self, e):
        self._data.append(e)
    def top(self):
        if self.is_empty():
            return "null"
        return self._data[-1]
    def pop(self):
        if self.is_empty():
            return "null"
        return self._data.pop()

stack = ArrayStack() #操作数栈
mem = [0 for i in range(100)] #内存
s1 = 0
s2 = 0
labels = {} #标号指令
pc_num = 0  # 指令计数
#带操组数
def withValue(strs):
    global stack,pc_num,labels
    if strs[0] == 'LOADI':
        stack.push(int(strs[1]))
    elif strs[0] == 'LOAD':
        stack.push(mem[int(strs[1])])
    elif strs[0] == 'STO':
        mem[int(strs[1])] = stack.top()
    elif strs[0] == 'BRF':
        if stack.top() == 0 or stack.top() == "null":
            pc_num = labels.get(strs[1])
        stack.pop()
    elif strs[0] == 'BR':
        pc_num = labels.get(strs[1])
#不带操作数
def withoutValue(strs):
    global stack,s1,s2
    if strs == 'POP':
        stack.pop()
    elif strs == 'LES':
        s1 = stack.top()
        stack.pop()
        s2 = stack.top()
        stack.pop()
        if s2 < s1:
            stack.push(1)
        else:
            stack.push(0)
    elif strs == 'IN':
        a = input("请输入：")
        stack.push(int(a))
    elif strs == 'ADD':
        s1 = stack.top()
        stack.pop()
        s2 = stack.top()
        stack.pop()
        stack.push(s1+s2)
    elif strs == 'SUB':
        s1 = stack.top()
        stack.pop()
        s2 = stack.top()
        stack.pop()
        stack.push(s2-s1)
    elif strs == 'MULT':
        s1 = stack.top()
        stack.pop()
        s2 = stack.top()
        stack.pop()
        stack.push(s1*s2)
    elif strs == 'DIV':
        stack.push(s2/s1)
    elif strs == 'EQ':
        s1 = stack.top()
        stack.pop()
        s2 = stack.top()
        stack.pop()
        if s1 == s2:
            stack.push(1)
        else:
            stack.push(0)
    elif strs == 'NOTEQ':
        s1 = stack.top()
        stack.pop()
        s2 = stack.top()
        stack.pop()
        if s1 == s2:
            stack.push(0)
        else:
            stack.push(1)
    elif strs == 'GT':
        s1 = stack.top()
        stack.pop()
        s2 = stack.top()
        stack.pop()
        if s2 > s1:
            stack.push(1)
        else:
            stack.push(0)
    elif strs == 'GE':
        s1 = stack.top()
        stack.pop()
        s2 = stack.top()
        stack.pop()
        if s2 >= s1:
            stack.push(1)
        else:
            stack.push(0)
    elif strs == 'LE':
        s1 = stack.top()
        stack.pop()
        s2 = stack.top()
        stack.pop()
        if s2 <= s1:
            stack.push(1)
        else:
            stack.push(0)
    elif strs == 'AND':
        s1 = stack.top()
        stack.pop()
        s2 = stack.top()
        stack.pop()
        stack.push(s1 and s2)
    elif strs == 'OR':
        s1 = stack.top()
        stack.pop()
        s2 = stack.top()
        stack.pop()
        stack.push(s1 or s2)
    elif strs == 'NOT':
        s1 = stack.top()
        stack.pop()
        if s1 == 0:
            stack.push(1)
        else:
            stack.push(0)
    elif strs == 'OUT':
        print("输出：{}".format(stack.top()))
        stack.pop()
    elif strs == 'STOP':
        print("程序结束")
        exit()

if __name__ == '__main__':
    f = open("中间代码.txt", 'r')
    str_files = f.readlines()
    codes = [[''] * 2 for i in range(len(str_files))]
    for i in str_files:
        strings = i.split(" ")
        if len(strings) == 2:
            codes[pc_num][0] = strings[0]
            codes[pc_num][1] = strings[1].strip('\n')
        elif len(strings) == 1:
            codes[pc_num][0] = strings[0]
            codes[pc_num][1] = ''
            if ':' in strings[0]:
                labels[strings[0].strip(':\n')] = pc_num
        pc_num = pc_num + 1
    length = pc_num
    pc_num = 0
    while pc_num < length:
        if codes[pc_num][1] == '':
            withoutValue(codes[pc_num][0].strip('\n'))
        else:
            withValue(codes[pc_num])
        pc_num = pc_num + 1

