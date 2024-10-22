import pytest
from flask import json
from Zepto_project.tests.app.main import app, Node, create_rule, evaluate_rule, combine_rules

@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_create_rule(client):
    """Test the create_rule endpoint."""
    response = client.post('/create_rule', json={'rule': 'age > 30'})
    assert response.status_code == 200
    assert 'operand' in response.get_json()['value']

def test_create_rule_missing_rule(client):
    """Test the create_rule endpoint with missing 'rule'."""
    response = client.post('/create_rule', json={})
    assert response.status_code == 400
    assert "Missing 'rule'" in response.get_json()["message"]

def test_evaluate_rule(client):
    """Test the evaluate_rule function."""
    ast = Node("operand", value='age > 30')
    user_data = {"age": 35}
    result = evaluate_rule(ast, user_data)
    assert result is True

def test_evaluate_rule_invalid_data(client):
    """Test the evaluate_rule endpoint with invalid user data."""
    ast = Node("operand", value='age > 30')
    user_data = {"age": "thirty-five"}  # Invalid data type
    result = evaluate_rule(ast, user_data)
    assert result is False  # Ensure it handles the invalid data gracefully

def test_combine_rules(client):
    """Test the combine_rules function."""
    rules = ["age > 30", "salary > 50000"]
    combined_ast = combine_rules(rules)
    assert combined_ast.type == "operator"
    assert combined_ast.value == "AND"

def test_combine_rules_empty_list(client):
    """Test the combine_rules function with an empty list."""
    combined_ast = combine_rules([])
    assert combined_ast is None  # Should return None for empty input
