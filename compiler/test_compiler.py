import pytest
import networkx as nx
from translator import lexer, parser, add_node, execute_parse_tree_testing
from globals import NODE_COUNTER, parseGraph

# Reset the global variables before each test
@pytest.fixture(autouse=True)
def reset_globals():
    global NODE_COUNTER, parseGraph
    NODE_COUNTER = 0
    parseGraph.clear()

# Test cases for the lexer
@pytest.mark.parametrize("test_input,expected_output", [
    ("3 + 4", [('NUMBER', 3), ('PLUS', '+'), ('NUMBER', 4)]),
    ("a = 3", [('VARIABLE', 'a'), ('SETTO', '='), ('NUMBER', 3)]),
    ("3 - 4", [('NUMBER', 3), ('MINUS', '-'), ('NUMBER', 4)]),
    ("3 * 4", [('NUMBER', 3), ('TIMES', '*'), ('NUMBER', 4)]),
    ("16 / 4", [('NUMBER', 16), ('DIVIDE', '/'), ('NUMBER', 4)]),
    ("16 ^ 4", [('NUMBER', 16), ('EXP', '^'), ('NUMBER', 4)]),
    ("(3 + 4)", [('LPAREN', '('), ('NUMBER', 3), ('PLUS', '+'), ('NUMBER', 4), ('RPAREN', ')')]),
    ("16 > 4", [('NUMBER', 16), ('GT', '>'), ('NUMBER', 4)]),
    ("16 < 4", [('NUMBER', 16), ('LT', '<'), ('NUMBER', 4)]),
    ("16 >= 4", [('NUMBER', 16), ('GE', '>='), ('NUMBER', 4)]),
    ("16 <= 4", [('NUMBER', 16), ('LE', '<='), ('NUMBER', 4)]),
    ("16 == 4", [('NUMBER', 16), ('EQ', '=='), ('NUMBER', 4)]),
    ("16 != 4", [('NUMBER', 16), ('NE', '!='), ('NUMBER', 4)]),
    ("if(2==2):1+1", [('IF', 'if'), ('LPAREN', '('), ('NUMBER', 2), ('EQ', '=='), ('NUMBER', 2), ('RPAREN', ')'), ('COLON', ':'), ('NUMBER', 1), ('PLUS', '+'), ('NUMBER', 1)]),
    ("(2==2) && (1!=1)", [('LPAREN', '('), ('NUMBER', 2), ('EQ', '=='), ('NUMBER', 2), ('RPAREN', ')'), ('AND', '&&'), ('LPAREN', '('), ('NUMBER', 1), ('NE', '!='), ('NUMBER', 1), ('RPAREN', ')')]),
    ("(2==2) || (1!=1)", [('LPAREN', '('), ('NUMBER', 2), ('EQ', '=='), ('NUMBER', 2), ('RPAREN', ')'), ('OR', '||'), ('LPAREN', '('), ('NUMBER', 1), ('NE', '!='), ('NUMBER', 1), ('RPAREN', ')')]),
    ("(3 + 4) * 5", [('LPAREN', '('), ('NUMBER', 3), ('PLUS', '+'), ('NUMBER', 4), ('RPAREN', ')'), ('TIMES', '*'), ('NUMBER', 5)])
    # Add more test cases for other tokens and inputs
])

def test_lexer(test_input, expected_output):
    lexer.input(test_input)
    result = [(tok.type, tok.value) for tok in lexer]
    print("Lexer result", result)
    assert result == expected_output

# Test cases for the parser
@pytest.mark.parametrize("test_input,expected_output", [
    ("3 + 4", "7"),
    ("7-5", "2"),
    # Add more test cases for different types of arithmetic expressions
])

def test_simple_arithmetic(test_input, expected_output, reset_globals):
    root = add_node({"type": "INITIAL", "label": "INIT"})
    result = parser.parse(test_input)
    parseGraph.add_edge(root["counter"], result["counter"])
    print("Graph structure (detailed):", parseGraph.nodes(data=True))
    tree_result = execute_parse_tree_testing(parseGraph)
    assert str(tree_result) == expected_output
