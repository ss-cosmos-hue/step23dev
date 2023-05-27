#! /usr/bin/python3
def myabs(value):
    return abs(value)
def myint(value):
    return int(value)
def myround(value):
    return round(value)
functions = {'abs':myabs,'int':myint,'round':myround}#lambda式使えるかも?


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


def read_plus(line, index):#疑問:read_plus の引数にlineがあるのはなぜ?
    token = {'type': 'PLUS'}
    return token, index + 1


def read_minus(line, index):
    token = {'type': 'MINUS'}
    return token, index + 1

def read_multiply(line,index):
    token = {'type': 'MULTIPLY'}
    return token, index + 1 

def read_divide(line,index):
    token = {'type':'DIVIDE'}
    return token, index + 1

def read_open_parenthesis(line,index):
    token = {'type':'OPENER'}
    return token, index + 1

def read_close_parenthesis(line,index):
    token = {'type':'CLOSER'}
    return token, index  + 1

def read_abs(line,index):
    token = {'type':'FUNCTION','effect':'abs'}
    return token, index + len('abs')

def read_int(line,index):
    token = {'type':'FUNCTION','effect':'int'}
    return token,index +len('int')

def read_round(line,index):
    token = {'type':'FUNCTION','effect':'round'}
    return token,index + len('round')

#Input: one line of equation
#Output: list of numbers and operators
def tokenize(line):
    tokens = []
    index = 0
    while index < len(line):
        if line[index].isdigit():
            (token, index) = read_number(line, index)#全てひとつにしよう
        elif line[index] == '+':
            (token, index) = read_plus(line, index)
        elif line[index] == '-':
            (token, index) = read_minus(line, index)
        elif line[index] == '*':
            (token, index) = read_multiply(line,index)
        elif line[index] == '/':
            (token,index) = read_divide(line,index)
        elif line[index] == '(':
            (token,index) = read_open_parenthesis(line,index)
        elif line[index] == ')':
            (token,index) =  read_close_parenthesis(line,index)
        elif line[index:index+len('abs')] == 'abs':
            (token,index) = read_abs(line,index)
        elif line[index:index+len('int')] ==  'int':
            (token,index) = read_int(line,index)
        elif line[index:index+len('round')] ==  'round':
            (token,index) = read_round(line,index)
        else:
            print('Invalid character found: ' + line[index])
            exit(1)
        tokens.append(token)
    return tokens

#Input: tokens(list of numbers and operators)
#Output: value of the equation
def evaluate(tokens):
    tokens.insert(0,{'type':'OPENER'})
    tokens.append({'type':'CLOSER'})
    while True:
        (tokens,has_parenthesis) = _pre_evaluate_innermost_parenthesis(tokens)
        if not has_parenthesis:
            break
    assert (len(tokens) == 1),tokens
    answer  = tokens[0]['number']
    return answer

#Input: tokens:  list of  numbers  and operators inside the innermost parenthesis
#               do  not have any parenthesis token
#Output: the evaluation of the equation inside parenthesis
def _pre_evaluate_innermost_parenthesis(tokens):
    new_tokens = []
    has_parenthesis = False 
    opener_idx,closer_idx =  None, None 
    index = 0
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
    value_in_parenthesis = _evaluate_partially(tokens[(opener_idx+1):(closer_idx)])
    if opener_idx  == 0 or tokens[opener_idx-1]['type']!='FUNCTION':
        new_tokens = tokens[:opener_idx]+[{'type':'NUMBER','number':value_in_parenthesis}]+tokens[closer_idx+1:]
        return (new_tokens,has_parenthesis)
    value_of_func = functions[tokens[opener_idx-1]['effect']](value_in_parenthesis)
    new_tokens = tokens[:opener_idx-1]+[{'type':'NUMBER','number':value_of_func}]+tokens[closer_idx+1:]
    return (new_tokens,has_parenthesis)
    
#Input: part of tokens
#return: value of the partial equation
def _evaluate_partially(tokens):
    answer = 0
    tokens.insert(0, {'type': 'PLUS'}) # Insert a dummy '+' token
    tokens = _pre_evaluate_mul_or_div(tokens,'DIVIDE')
    tokens = _pre_evaluate_mul_or_div(tokens,'MULTIPLY')
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
def _pre_evaluate_mul_or_div(tokens,operator):
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
    test("1")
    # test("1+2")
    # test("1.0+2.1-3")
    # test("3/2")
    # test("3/2/2")
    # test("3*2")
    # test("3*2*2")
    # test("3*2/4*2")
    # test("1+3*2/4*2+1")
    # test("3.0+4*2-1/5")
    print("==== Test finished! ====\n")

run_test()

while True:
    print('> ', end="")
    line = input()
    tokens = tokenize(line)
    answer = evaluate(tokens)
    print("answer = %f\n" % answer)