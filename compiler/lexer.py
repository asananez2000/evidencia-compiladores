import ply.lex as lex

symbol_table = dict()

symbol_table["e"] = 2.718281828459045

PLUS_OP = 1
MINUS_OP = 2
TIMES_OP = 3
DIVIDE_OP = 4


tokens = (
    'NUMBER',
    'VARIABLE',
    'SETTO',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE'
)

t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_SETTO = r'='


def t_NUMBER(t):
    r'\d+'
    t.value = float(t.value)
    return t

def t_VARIABLE(t):
    r'[A-Za-z]([A-Za-z0-9_])*'
    return t

# ------------ boilerplate 
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
t_ignore = ' \t'

def t_error(t):
    print("Error on analysis")
    t.lexer.skip(1)
### ---------- end 


lexer = lex.lex()

while True:

    try:
        data = input(">")

        if(data == 'exit'):
            break
        
        if(data == 'symbols'):
            print(symbol_table)
            continue
            
        lexer.input(data)
    except EOFError:
        break
    
    possible_assignment = 0
    last_var = ""
    possible_result = 0
    possible_op = 0

    while True:
        tok = lexer.token()
        if not tok:
            if(possible_assignment == 1):
                if( last_var not in symbol_table ):
                    print("DUDE!! No symbol on table!")
                else:
                    print( symbol_table[last_var] )
            if(possible_op > 0):
                print(possible_result)
            break
        
        if( tok.type == "SETTO"):
            if(possible_assignment == 1):
                possible_assignment = 2

        if( tok.type == "PLUS"):
            if(possible_assignment == 1): #override
                possible_assignment = 0
                possible_result = symbol_table[last_var]

            possible_op = PLUS_OP

        if( tok.type == "MINUS"):
            if(possible_assignment == 1): #override
                possible_assignment = 0
                possible_result = symbol_table[last_var]

            possible_op = MINUS_OP
        
        if( tok.type == "TIMES"):
            possible_op = TIMES_OP
        
        if( tok.type == "DIVIDE"):
            possible_op = DIVIDE_OP
            

        if( tok.type == "NUMBER"):
            if(possible_assignment == 2):
                symbol_table[last_var] = tok.value
                possible_assignment = 0
            else:
                if(possible_op == PLUS_OP): # its a sum
                    possible_result += tok.value
                if(possible_op == MINUS_OP): # its a subtraction
                    possible_result -= tok.value    
                if(possible_op == TIMES_OP): # its a subtraction
                    possible_result *= tok.value    
                if(possible_op == DIVIDE_OP): # its a subtraction
                    possible_result /= tok.value    
                if(possible_op == 0): # its a sum
                    possible_result = tok.value
                

        if( tok.type == "VARIABLE"):
            if(possible_assignment == 2):
                symbol_table[last_var] = symbol_table[tok.value]
            else:
                if(possible_op > 0):
                    if tok.value in symbol_table:
                        if(possible_op == PLUS_OP): # its a sum
                            possible_result += symbol_table[tok.value]
                        if(possible_op == MINUS_OP): # its a sum
                            possible_result -= symbol_table[tok.value]
                        if(possible_op == TIMES_OP): # its a sum
                            possible_result *= symbol_table[tok.value]
                        if(possible_op == DIVIDE_OP): # its a sum
                            possible_result /= symbol_table[tok.value]
                    
                    else:
                        print("ERROR! No symbol found")
                else:
                    print(tok.value)
                    if( tok.value in ['e','pi'] ):
                        tok.value = tok.value + '_var'
                        print("Unable to assign variable, new value assigned to " , tok.value) 
                    possible_assignment = 1
                    last_var = tok.value
            
            
print("Finished, accepted")