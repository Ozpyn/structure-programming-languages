from tokenizer import tokenize
from parser import parse


def evaluate(ast, environment):
    if ast["tag"] == "number":
        assert type(ast["value"]) in [
            float,
            int,
        ], f"unexpected ast numeric value {ast['value']} is a {type(ast['value'])}."
        return ast["value"], False
    if ast["tag"] == "+":
        left_value, _ = evaluate(ast["left"], environment)
        right_value, _ = evaluate(ast["right"], environment)
        return left_value + right_value, False
    if ast["tag"] == "-":
        left_value, _ = evaluate(ast["left"], environment)
        right_value, _ = evaluate(ast["right"], environment)
        return left_value - right_value, False
    if ast["tag"] == "*":
        left_value, _ = evaluate(ast["left"], environment)
        right_value, _ = evaluate(ast["right"], environment)
        return left_value * right_value, False
    if ast["tag"] == "/":
        left_value, _ = evaluate(ast["left"], environment)
        right_value, _ = evaluate(ast["right"], environment)
        return left_value / right_value, False
    if ast["tag"] == "negate":
        value, _ = evaluate(ast["value"], environment)
        return -value, False
    if ast["tag"] == "mod":
        left_value, _ = evaluate(ast["left"], environment)
        right_value, _ = evaluate(ast["right"], environment)
        while left_value >= right_value:
            left_value -= right_value
        return left_value, False
        # return left_value % right_value, False
    if ast["tag"] == "not":
        value, _ = evaluate(ast["value"], environment)
        return 1 if not value else 0, False
    raise Exception(f"Unknown token in AST: {ast['tag']}")


def equals(code, environment, expected_result, expected_environment=None):
    result, _ = evaluate(parse(tokenize(code)), environment)
    assert (
        result == expected_result
    ), f"""ERROR: When executing-- 
        {[code]},
        --expected--
        {[expected_result]},
        --got--
        {[result]}."""
    if expected_environment:
        assert (
            environment == expected_environment
        ), f"""
        ERROR: When executing 
        {[code]}, 
        expected
        {[expected_environment]},\n got \n{[environment]}.
        """


def test_evaluate_single_value():
    print("test evaluate single value")
    equals("4", {}, 4, {})


def test_evaluate_addition():
    print("test evaluate addition")
    equals("1+3", {}, 4)
    equals("1+4", {}, 5)
    equals("4+2", {}, 6)
    equals("4+2+1", {}, 7)


def test_evaluate_subtraction():
    print("test evaluate subtraction")
    equals("11-5", {}, 6)


def test_evaluate_multiplication():
    print("test evaluate multiplication")
    equals("11*5", {}, 55)


def test_evaluate_division():
    print("test evaluate division")
    equals("12/3", {}, 4)


def test_evaluate_unary_negation():
    print("test evaluate unary negation")
    equals("-12/3", {}, -4)
    equals("12/-3", {}, -4)
    equals("12/--3", {}, 4)
    equals("(3+4)--(1+2)", {}, 10)


def test_evaluate_modulus():
    print("test evaluate modulus")
    equals("13%2", {}, 1)
    equals("25%3", {}, 1)
    equals("23%6", {}, 5)
    equals("20%5", {}, 0)


def test_evaluate_not_negation():
    print("test evaluate not negation")
    equals("!0", {}, 1)
    equals("!1", {}, 0)
    equals("!12", {}, 0)


def test_evaluate_complex_expression():
    print("test evaluate complex expression")
    equals("(3+4)-(1+2)", {}, 4)
    equals("3+4*2", {}, 11)
    equals("(1+2)*3", {}, 9)
    equals("(1+2)/(3*1)", {}, 1)


if __name__ == "__main__":
    test_evaluate_single_value()
    test_evaluate_addition()
    test_evaluate_subtraction()
    test_evaluate_multiplication()
    test_evaluate_division()
    test_evaluate_unary_negation()
    test_evaluate_modulus()
    test_evaluate_not_negation()
    test_evaluate_complex_expression()
    print("done")
