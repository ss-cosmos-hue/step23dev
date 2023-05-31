#! /usr/bin/python3
#non-numeric input
FUNCTIONS = {'abs':lambda x: abs(x),'int':lambda x: int(x),'round':lambda x:round(x)}
OPERATORS = {'+':'PLUS','-':'MINUS','*':'MULTIPLY','/':'DIVIDE'}
PARENTHESES = {'(':'OPENER',')':'CLOSER'}

#Given  line and index where the first charaacter of a certain sign is found, 
#   return the token of the sign and incremented index(, where the next token starts)
#Note:  read_{type}(line,index) function is used only when the corresponding sign or 
#                   string is determined to be starting at the index of the line
def read_number(line, index):
    number = 0
    while index < len(line) and line[index].isdigit():
        number = number * 10 + int(line[index])
        index += 1
    if index < len(line) and line[index] == '.':
        index += 1
        decimal = 0.1
        while index < len(line) and line[index].isdigit():
            number += int(line[index]) * decimal
            decimal /= 10
            index += 1
    token = {'type': 'NUMBER', 'number': number}
    return token, index

def read_operator(line,index):#疑問:read_plus の引数にlineがあるのはなぜ?
    token = {'type': OPERATORS[line[index]]}
    return token, index + 1

def read_parenthesis(line,index):
    token = {'type':PARENTHESES[line[index]]}
    return token, index + 1

def read_function(line,index,function_name):
    token = {'type':'FUNCTION','effect':function_name}
    return token, index +len(function_name)

#Input:  index and line to focus on  the index of the line
#Output: (the existence of function,function_name or None)
#        if there is no function found starting at the index, return (False, None)
#Note:  unlike  "is_digit()", this function returns function name in addition to True or False
#        to avoid looking at the substring of the line twice
def maybe_find_function(line,index):
    for function_name in FUNCTIONS:
        if line[index:index+len(function_name)] == function_name:
            return (True ,function_name)
    return (False,None)

#Given a string to interpret as an equation, break the string into tokens
#Input: one line of equation
#Output: list of numbers, operators, parentheses, functions
def tokenize(line):
    tokens = []
    index = 0
    while index < len(line):
        if line[index].isdigit():
            (token, index) = read_number(line, index)
        elif line[index] in OPERATORS.keys():
            (token,index)  = read_operator(line,index)
        elif line[index] in PARENTHESES.keys() :
            (token,index) = read_parenthesis(line,index)
        elif ((tuple_isfound_and_funcname  := maybe_find_function(line,index)) and tuple_isfound_and_funcname[0] == True):
            (token,index) = read_function(line,index,tuple_isfound_and_funcname[1])
        else:
            print('Invalid character found: ' + line[index])
            exit(1)
        tokens.append(token)
    return tokens

#Given tokens, return the value of the equation
#Input: tokens(list of numbers and operators)
#Output: value of the equation
def evaluate(tokens):
    tokens.insert(0,{'type':'OPENER'})#envelope the equation with a dummy pair of parentheses for the sake of generalization
    tokens.append({'type':'CLOSER'})
    while True:
        (tokens,has_parenthesis) = _process_token_about_innermost_parenthesis(tokens)
        if not has_parenthesis:
            break
    assert (len(tokens) == 1),tokens
    answer  = tokens[0]['number']
    return answer

#Input: tokens:  list of  numbers  and operators
#Output: updated_tokens: the evaluation of the equation inside parenthesis 
#        has_parenthesis: whether  or not the  given token has parentheses
#                         if not, do not update tokens and return given tokens
def _process_token_about_innermost_parenthesis(tokens):
    new_tokens = []
    has_parenthesis = False 
    opener_idx,closer_idx =  None, None 
    index = 0
    
    #find 'CLOSER' parenthesis
    while index < len(tokens):
        if tokens[index]['type'] == 'OPENER':
            opener_idx  = index
            has_parenthesis = True
        if tokens[index]['type'] == 'CLOSER':
            closer_idx  = index 
            break 
        index += 1 
    if not has_parenthesis:
        original_tokens = tokens 
        assert(len(original_tokens)==1)
        return (tokens,has_parenthesis)
    assert(opener_idx+1<=closer_idx-1)

    value_in_parenthesis = _evaluate_token_inside_parenthesis(tokens[(opener_idx+1):(closer_idx)])
    if opener_idx  == 0 or tokens[opener_idx-1]['type']!='FUNCTION':
        new_tokens = tokens[:opener_idx]+[{'type':'NUMBER','number':value_in_parenthesis}]+tokens[closer_idx+1:]
        return (new_tokens,has_parenthesis)
    
    value_of_func = FUNCTIONS[tokens[opener_idx-1]['effect']](value_in_parenthesis)
    new_tokens = tokens[:opener_idx-1]+[{'type':'NUMBER','number':value_of_func}]+tokens[closer_idx+1:]
    return (new_tokens,has_parenthesis)
    
#Input: tokens inside the innermost parenthesis at that time
#       tokens should be without any parenthesis token
#return: value of the partial equation
def _evaluate_token_inside_parenthesis(tokens):
    answer = 0
    tokens.insert(0, {'type': 'PLUS'}) # Insert a dummy '+' token
    tokens = _process_token_about_mul_or_div(tokens,'DIVIDE')
    tokens = _process_token_about_mul_or_div(tokens,'MULTIPLY')
    index = 1
    while index < len(tokens):
        if tokens[index]['type'] == 'NUMBER':
            if tokens[index - 1]['type'] == 'PLUS':
                answer += tokens[index]['number']
            elif tokens[index - 1]['type'] == 'MINUS':
                answer -= tokens[index]['number']
            else:
                print('Invalid syntax')
                exit(1)
        index += 1
    return answer

#Input: tokens: list of numbers and operators
#       operator: string of operator to evaluate// either 'DIVIDE' or 'MULTIPLY'
#Output:tokens of equations where the designated operator is evaluated
def _process_token_about_mul_or_div(tokens,operator):
    assert(operator == 'DIVIDE' or operator == 'MULTIPLY')
    tokens.append({'type': 'END'})#to avoid causing error by looling at tokens[index+1]
    new_tokens = []
    index = 0 # index of item in old_tokens under observance
    while index <len(tokens):
        if tokens[index]['type'] == 'END':
            break
        elif tokens[index]['type'] == 'NUMBER':
            new_number = tokens[index]['number']
            if tokens[index+1]['type'] == operator:
                while tokens[index+1]['type'] == operator and tokens[index+2]['type'] == 'NUMBER':
                    if operator == 'DIVIDE':
                        new_number /= tokens[index+2]['number']
                    elif operator == 'MULTIPLY':
                        new_number *= tokens[index+2]['number']
                    index += 2 
            new_tokens.append({'type':'NUMBER','number':new_number}) 
            index += 1 
        else:
            new_tokens.append(tokens[index])
            index += 1          
    return new_tokens

def test(line):
    tokens = tokenize(line)
    actual_answer = evaluate(tokens)
    expected_answer = eval(line)
    if abs(actual_answer - expected_answer) < 1e-8:
        print("PASS! (%s = %f)" % (line, expected_answer))
    else:
        print("FAIL! (%s should be %f but was %f)" % (line, expected_answer, actual_answer))


# Add more tests to this function :)
def run_test():
    print("==== Test started! ====")
    #整数演算
    test("1")        #演算なし
    test("1+2")      #足し算        
    test("5-2")      #引き算
    test("3-1+2-5")  #両方
    #小数を含む演算
    test("3.0")
    test("1.0+2.0+4")
    test("1.0-2.1")
    test("3.0+2.0-5")
    #除算
    test("3/2")
    test("3/2/2")
    #乗算
    test("3*2")
    test("3*2*2")
    #除算と乗算を含む
    test("3*2/4*2")
    #四則演算
    test("1+3*2/4*2+1")
    test("3.0+4*2-1/5") #小数あり
    #括弧付き
    test("5+(3+4.0+2)") #カッコひとつ
    test("(4+2)/3+2*(5-1)")#カッコ２つ
    test("(5+(3+4.0)+2)*4") #カッコ入れ子
    #関数あり
    test("abs(-2)")
    test("abs(2)")
    test("int(2.3)")
    test("int(2.5)")
    test("int(2.7)")
    test("int(-2.3)")
    test("int(-2.5)")
    test("int(-2.7)")
    test("round(2.3)")
    test("round(2.5)")
    test("round(2.7)")
    test("round(-2.3)")
    test("round(-2.5)")
    test("round(-2.7)")
    test("abs(-2+4-5.0)+int(2.3-4)+round(5.2-4)")#関数の引数が式
    test("abs(-2+(4-5.0)*2+int(2.3-4))*round(5.2-4)")#関数がカッコのなか
    #全て使う
    test("round(abs(2.3-1)*(round(3.2*56-100)+int(3.0*5/6)))")
    print("==== Test finished! ====\n")

run_test()

while True:
    print('> ', end="")
    line = input()
    tokens = tokenize(line)
    answer = evaluate(tokens)
    print("answer = %f\n" % answer)