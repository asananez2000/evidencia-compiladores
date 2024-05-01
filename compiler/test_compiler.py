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
    ("if(2==2): 3 else: 1+1", [('IF', 'if'), ('LPAREN', '('), ('NUMBER', 2), ('EQ', '=='), ('NUMBER', 2), ('RPAREN', ')'), ('COLON', ':'), ('NUMBER', 3), ('ELSE', 'else'), ('COLON', ':'), ('NUMBER', 1), ('PLUS', '+'), ('NUMBER', 1)]),
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
    ("7 - 5", "2"),
    ("6 * 9", "54"),
    ("8 / 2", "4.0"),
    ("2 ^ 3", "8"),
    ("2 * (3 + 4)", "14"),
    ("10 + 5", "15"),
    ("15 - 8", "7"),
    ("4 * 7", "28"),
    ("10 / 3", "3.3333333333333335"),
    ("5 ^ 2", "25"),
    ("(2 + 3) * 4", "20"),
    ("2 + 3 * 4", "14"),
    ("(2 + 3) * (4 + 5)", "45"),
    ("(10 + 5) / (3 - 1)", "7.5"),
    ("(2 ^ 3) + (4 * 5)", "28"),
    ("(10 + 5) / (3 - 1) + 2", "9.5"),
    ("(2 + 3) * (4 + 5) - 10", "35"),
    ("(2 + 3) * (4 + 5) / 2", "22.5")
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
    ("z = 44 + 2", "46"),
    ("a = 10", "10"),
    ("b = 5 + 3", "8"),
    ("c = a * b", "80"),
    ("d = c / 2", "40.0"),
    ("e = d - 10", "30.0")
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
    ("((5 > 3) && (2 < 3)) || ((4 > 2) && (1 < 5))", "True"),
    ("((5 > 3) && (2 < 3)) || ((4 > 2) && (1 > 5))", "True"),
    ("((5 > 3) && (2 > 3)) || ((4 > 2) && (1 < 5))", "True"),
    ("((5 > 3) && (2 > 3)) || ((4 > 2) && (1 > 5))", "False"),
    ("((5 > 3) || (2 < 3)) && ((4 > 2) || (1 < 5))", "True"),
    ("((5 > 3) || (2 < 3)) && ((4 > 2) || (1 > 5))", "True"),
    ("((5 > 3) || (2 > 3)) && ((4 > 2) || (1 < 5))", "True"),
    ("((5 > 3) || (2 > 3)) && ((4 > 2) || (1 > 5))", "True")
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
    ("if (1!=1): 8-10 else: 9+14", "23"),
    ("if (1==1): 8-10 else: 9+14", "-2"),
    ("if (2 == 2): 10 else: 0", "10"),
    ("if (4 > 8): 4 else: 8", "8"),
    ("(33 > 22)?(3):(0)", "3"),
    ("(4 != 4)?(4):(100)", "100"),
    ("(5 >= 10)?(32):(0)", "0"),
    ("(2 < 5)?(10):(20)", "10"),
    ("(7 >= 7)?(100):(200)", "100"),
    ("if (3 > 2): 5+5 else: 2-1", "10"),
    ("if (8 <= 10): 3*3 else: 4/2", "9"),
    ("(6 == 6)?(8):(9)", "8"),
    ("(1 != 2)?(100):(200)", "100"),
    ("(4 > 7)?(1):(2)", "2"),
    ("(5 >= 5)?(10):(20)", "10"),
    ("if (2 < 3): 4*4 else: 5-1", "16"),
    ("if (9 <= 10): 6/2 else: 8*2", "3.0"),
    ("(7 == 7)?(5):(10)", "5"),
    ("(3 != 3)?(100):(200)", "200"),
    ("(6 > 9)?(1):(2)", "2"),
    ("(5 >= 6)?(1):(2)", "2"),
    ("if (4 == 4): 7+7 else: 8-2", "14")
])

def test_conditional_statements(test_input, expected_output, reset_globals):
    root = add_node({"type": "INITIAL", "label": "INIT"})
    result = parser.parse(test_input)
    parseGraph.add_edge(root["counter"], result["counter"])
    print("Graph structure (detailed):", parseGraph.nodes(data=True))
    tree_result = execute_parse_tree_testing(parseGraph)
    assert str(tree_result) == expected_output