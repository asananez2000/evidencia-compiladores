import pytest
import networkx as nx
import numpy as np
import cv2 
from translator import lexer, parser, add_node, execute_parse_tree_testing
from globals import NODE_COUNTER, parseGraph

# Reset the global variables before each test
@pytest.fixture(autouse=True)
def reset_globals():
    global NODE_COUNTER, parseGraph
    NODE_COUNTER = 0
    parseGraph.clear()
    assert NODE_COUNTER == 0
    assert len(parseGraph) == 0

# --------------------- TEST CASES FOR LEXER --------------------
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
])

def test_lexer(test_input, expected_output):
    lexer.input(test_input)
    result = [(tok.type, tok.value) for tok in lexer]
    print("Lexer result", result)
    assert result == expected_output

# --------------------- TEST CASES FOR PARSER --------------------
# Test cases for simple arithmetic operations
@pytest.mark.parametrize("test_input,expected_output", [
    ("3 + 4", "7"),
    ("7-5", "2"),
    ("6 * 9", "54"),
    ("8 / 2", "4.0"),
    ("2 ^ 3", "8"),
    ("2 * (3 + 4)", "14")
])

def test_simple_arithmetic(test_input, expected_output, reset_globals):
    root = add_node({"type": "INITIAL", "label": "INIT"})
    result = parser.parse(test_input)
    parseGraph.add_edge(root["counter"], result["counter"])
    print("Graph structure (detailed):", parseGraph.nodes(data=True))
    tree_result = execute_parse_tree_testing(parseGraph)
    assert str(tree_result) == expected_output

# Test cases for variable assignment
@pytest.mark.parametrize("test_input,expected_output", [
    ("x = 5", "5"),
    ("y = x + 2", "7"),
])

def test_variable_assignment(test_input, expected_output, reset_globals):
    root = add_node({"type": "INITIAL", "label": "INIT"})
    result = parser.parse(test_input)
    parseGraph.add_edge(root["counter"], result["counter"])
    print("Graph structure (detailed):", parseGraph.nodes(data=True))
    tree_result = execute_parse_tree_testing(parseGraph)
    assert str(tree_result) == expected_output

# Test cases for comparison operators
@pytest.mark.parametrize("test_input,expected_output", [
    ("10 > 5", "True"),
    ("5 < 10", "True"),
    ("10 >= 10", "True"),
    ("5 <= 5", "True"),
    ("10 == 10", "True"),
    ("10 != 5", "True"),
    ("10 > 15", "False"),
    ("5 < 1", "False"),
    ("9 >= 10", "False"),
    ("6 <= 5", "False"),
    ("10 == 1", "False"),
    ("10 != 10", "False"),
])

def test_comparison_operators(test_input, expected_output, reset_globals):
    root = add_node({"type": "INITIAL", "label": "INIT"})
    result = parser.parse(test_input)
    parseGraph.add_edge(root["counter"], result["counter"])
    print("Graph structure (detailed):", parseGraph.nodes(data=True))
    tree_result = execute_parse_tree_testing(parseGraph)
    assert str(tree_result) == expected_output

# Test cases for logical operators
@pytest.mark.parametrize("test_input,expected_output", [
    ("(5 > 3) && (2 < 3)", "True"),
    ("(5 < 3) || (2 < 3)", "True"),
    ("(5 > 3) && (2 > 3)", "False"),
    ("(5 < 3) || (2 > 3)", "False"),
])

def test_logical_operators(test_input, expected_output, reset_globals):
    root = add_node({"type": "INITIAL", "label": "INIT"})
    result = parser.parse(test_input)
    parseGraph.add_edge(root["counter"], result["counter"])
    print("Graph structure (detailed):", parseGraph.nodes(data=True))
    tree_result = execute_parse_tree_testing(parseGraph)
    assert str(tree_result) == expected_output
    
# Test cases for string handling
@pytest.mark.parametrize("test_input,expected_output", [
    ("\"Hello, World!\"", "Hello, World!"),
    ("\"Hola Joeee\"", "Hola Joeee"),
])

def test_string_handling(test_input, expected_output, reset_globals):
    root = add_node({"type": "INITIAL", "label": "INIT"})
    result = parser.parse(test_input)
    parseGraph.add_edge(root["counter"], result["counter"])
    print("Graph structure (detailed):", parseGraph.nodes(data=True))
    tree_result = execute_parse_tree_testing(parseGraph)
    assert str(tree_result) == expected_output
    
# Test cases for function calls
@pytest.mark.parametrize("test_input,expected_output", [
    #("print()", "None"),
    ("max(1, 2)", "2"),
    ("max(1, max(2, 3))", "3"),
    ("load_image(\"test.jpg\")", cv2.imread("test.jpg")),
    ("search_cv2(\"GaussianBlur\")", str(getattr(cv2, "GaussianBlur"))),
    ("search_cv2(\"non_existent_function\")", 'None'),
    ("gen_matrix(2, 3, 1, 2, 3, 4, 5, 6)", np.array([[1, 2, 3], [4, 5, 6]])),
    ("gen_vector(1, 2, 3, 4)", np.array([1, 2, 3, 4])),
])

def test_function_calls(test_input, expected_output, reset_globals):
    root = add_node({"type": "INITIAL", "label": "INIT"})
    result = parser.parse(test_input)
    parseGraph.add_edge(root["counter"], result["counter"])
    print("Graph structure (detailed):", parseGraph.nodes(data=True))
    tree_result = execute_parse_tree_testing(parseGraph)
    if isinstance(expected_output, np.ndarray):
        assert np.array_equal(tree_result, expected_output)
    else:
        assert str(tree_result) == expected_output

# Test cases for conditional statements
@pytest.mark.parametrize("test_input,expected_output", [
    ("if((10==10)):10", "10"),
    ("if((10==20)): 8 + 11", "None"),
    ("if((2==1) && (2>1)): 10 + 9", "None"),
    ("if((2==1) || (2>1)): 10 + 9", "19"),
])

def test_conditional_statements(test_input, expected_output, reset_globals):
    root = add_node({"type": "INITIAL", "label": "INIT"})
    result = parser.parse(test_input)
    parseGraph.add_edge(root["counter"], result["counter"])
    print("Graph structure (detailed):", parseGraph.nodes(data=True))
    tree_result = execute_parse_tree_testing(parseGraph)
    assert str(tree_result) == expected_output