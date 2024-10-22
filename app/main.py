from flask import Flask, request, jsonify, abort
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from redis import Redis
from config import Config
import logging
from flask_cors import CORS

# Create Flask app
app = Flask(__name__)
CORS(app)
app.config.from_object(Config)

# Initialize Redis client with config
redis_client = Redis(host=app.config['REDIS_HOST'], port=app.config['REDIS_PORT'], db=app.config['REDIS_DB'])

# Initialize Flask Limiter with Redis as storage
limiter = Limiter(
    key_func=get_remote_address,
    storage_uri='redis://localhost:6379',
)
limiter.init_app(app)  # Initialize the limiter with the app

# Configure logging
logging.basicConfig(level=logging.INFO)

@app.route('/create_rule', methods=['POST'])
def create_rule_endpoint():
    """Endpoint to create a rule from a given rule string.

    Returns:
        JSON response with the created AST.
    """
    rule_string = request.json.get('rule')
    if not rule_string:
        logging.error("Missing 'rule' in request body.")
        return abort(400, description="Missing 'rule' in request body.")
    
    try:
        ast = create_rule(rule_string)
        logging.info("Rule created successfully.")
        return jsonify(ast), 200
    except Exception as e:
        logging.error(f"Error creating rule: {e}")
        return abort(500, description="Internal Server Error")

@app.route('/combine_rules', methods=['POST'])
def combine_rules_endpoint():
    """Endpoint to combine multiple rules into a single AST.

    Returns:
        JSON response with the combined AST.
    """
    rules = request.json.get('rules')
    if not rules:
        logging.error("Missing 'rules' in request body.")
        return abort(400, description="Missing 'rules' in request body.")
    
    try:
        combined_ast = combine_rules(rules)
        logging.info("Rules combined successfully.")
        return jsonify(combined_ast), 200
    except Exception as e:
        logging.error(f"Error combining rules: {e}")
        return abort(500, description="Internal Server Error")

@app.route('/evaluate_rule', methods=['POST'])
@limiter.limit("5 per minute")  # Limit to 5 requests per minute
def evaluate_rule_endpoint():
    """Endpoint to evaluate a rule based on user data.

    Returns:
        JSON response with the evaluation result.
    """
    ast = request.json.get('ast')
    user_data = request.json.get('user_data')

    if not ast or not isinstance(user_data, dict):
        logging.error("Invalid input data. Ensure 'ast' and 'user_data' are provided.")
        return abort(400, description="Invalid input data. Ensure 'ast' and 'user_data' are provided.")

    try:
        result = evaluate_rule(ast, user_data)
        logging.info("Rule evaluated successfully.")
        return jsonify({"result": result}), 200
    except Exception as e:
        logging.error(f"Error evaluating rule: {e}")
        return abort(500, description="Internal Server Error")

# Rule parsing and evaluation functions
def create_rule(rule_string):
    """Parses a rule string into an Abstract Syntax Tree (AST).

    Args:
        rule_string (str): The rule string to parse.

    Returns:
        Node: The root node of the generated AST.
    """
    tokens = rule_string.replace('(', ' ( ').replace(')', ' ) ').split()
    stack = []
    current_node = None
    temp_operand = []

    for token in tokens:
        if token == '(':
            stack.append(current_node)
            current_node = None
        elif token == ')':
            if temp_operand:
                operand_node = Node("operand", value=' '.join(temp_operand))
                if current_node and current_node.type == "operator":
                    current_node.right = operand_node
                else:
                    current_node = operand_node
                temp_operand = []

            if stack:
                parent_node = stack.pop()
                if parent_node and parent_node.type == "operator" and current_node:
                    parent_node.right = current_node
                    current_node = parent_node
        elif token in ['AND', 'OR']:
            if temp_operand:
                operand_node = Node("operand", value=' '.join(temp_operand))
                if current_node:
                    current_node.right = operand_node
                temp_operand = []

            operator_node = Node("operator", value=token)
            if current_node:
                operator_node.left = current_node
            current_node = operator_node
        else:
            temp_operand.append(token)

    if temp_operand:
        operand_node = Node("operand", value=' '.join(temp_operand))
        if current_node and current_node.type == "operator":
            current_node.right = operand_node
        else:
            current_node = operand_node

    if current_node is None:
        logging.warning("No valid AST created.")
    
    return current_node

def evaluate_rule(ast, user_data):
    """Evaluates the rule represented by the AST against user data.

    Args:
        ast (Node): The root of the AST.
        user_data (dict): A dictionary of user data to evaluate against.

    Returns:
        bool: The result of the evaluation.
    """
    if ast.type == "operator":
        left_eval = evaluate_rule(ast.left, user_data)
        right_eval = evaluate_rule(ast.right, user_data)
        if ast.value == "AND":
            return left_eval and right_eval
        elif ast.value == "OR":
            return left_eval or right_eval
    elif ast.type == "operand":
        field, operator, value = ast.value.split(' ', 2)
        value = int(value) if value.isdigit() else value.strip("'")
        if field not in user_data:
            logging.error(f"Field '{field}' not found in user data.")
            return False  # Return false if field is missing in user data
        if operator == '>':
            return user_data[field] > value
        elif operator == '<':
            return user_data[field] < value
        elif operator == '=':
            return user_data[field] == value
    return False

def combine_rules(rules):
    """Combines multiple rules into a single AST.

    Args:
        rules (list): A list of rule strings.

    Returns:
        Node: The root node of the combined AST.
    """
    if len(rules) == 0:
        logging.warning("No rules provided for combination.")
        return None
    
    combined_ast = create_rule(rules[0])
    for rule in rules[1:]:
        new_ast = create_rule(rule)
        combined_ast = Node("operator", left=combined_ast, right=new_ast, value="AND")
    
    return combined_ast

class Node:
    """Represents a node in the AST."""
    def __init__(self, node_type, left=None, right=None, value=None):
        self.type = node_type
        self.left = left
        self.right = right
        self.value = value

    def __repr__(self):
        return f"Node(type={self.type}, value={self.value}, left={self.left}, right={self.right})"

if __name__ == "__main__":
    combined_ast = combine_rules(["age > 30", "salary > 50000", "department = 'Sales'"])
    print("Combined AST:", combined_ast)

    user_data = {"age": 35, "salary": 60000, "department": "Sales"}
    result = evaluate_rule(combined_ast, user_data)
    print("Evaluation Result for Combined Rules:", result)

    app.run(debug=True)
