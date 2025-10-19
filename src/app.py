"""
Main Flask Application
"""
from flask import Flask, jsonify, request
from typing import Dict, Any
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')


class Calculator:
    """Simple calculator class for demonstration"""
    
    @staticmethod
    def add(a: float, b: float) -> float:
        """Add two numbers"""
        return a + b
    
    @staticmethod
    def subtract(a: float, b: float) -> float:
        """Subtract two numbers"""
        return a - b
    
    @staticmethod
    def multiply(a: float, b: float) -> float:
        """Multiply two numbers"""
        return a * b
    
    @staticmethod
    def divide(a: float, b: float) -> float:
        """Divide two numbers"""
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b


@app.route('/')
def home() -> Dict[str, Any]:
    """Home endpoint"""
    return jsonify({
        'status': 'success',
        'message': 'Welcome to Python CI/CD Demo',
        'version': '1.0.0'
    })


@app.route('/health')
def health() -> Dict[str, str]:
    """Health check endpoint"""
    return jsonify({'status': 'healthy'})


@app.route('/calculate', methods=['POST'])
def calculate() -> Dict[str, Any]:
    """Calculate endpoint"""
    try:
        data = request.get_json()
        operation = data.get('operation')
        a = float(data.get('a', 0))
        b = float(data.get('b', 0))
        
        calc = Calculator()
        
        operations = {
            'add': calc.add,
            'subtract': calc.subtract,
            'multiply': calc.multiply,
            'divide': calc.divide
        }
        
        if operation not in operations:
            return jsonify({
                'status': 'error',
                'message': 'Invalid operation'
            }), 400
        
        result = operations[operation](a, b)
        
        return jsonify({
            'status': 'success',
            'result': result
        })
        
    except ValueError as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Internal server error'
        }), 500


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('DEBUG', 'False').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)
