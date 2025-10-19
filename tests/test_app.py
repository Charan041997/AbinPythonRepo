"""
Unit tests for the application
"""
import pytest
from src.app import app, Calculator


@pytest.fixture
def client():
    """Create test client"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


class TestCalculator:
    """Test Calculator class"""
    
    def test_add(self):
        """Test addition"""
        calc = Calculator()
        assert calc.add(2, 3) == 5
        assert calc.add(-1, 1) == 0
        assert calc.add(0, 0) == 0
    
    def test_subtract(self):
        """Test subtraction"""
        calc = Calculator()
        assert calc.subtract(5, 3) == 2
        assert calc.subtract(1, 1) == 0
        assert calc.subtract(0, 5) == -5
    
    def test_multiply(self):
        """Test multiplication"""
        calc = Calculator()
        assert calc.multiply(2, 3) == 6
        assert calc.multiply(-2, 3) == -6
        assert calc.multiply(0, 5) == 0
    
    def test_divide(self):
        """Test division"""
        calc = Calculator()
        assert calc.divide(6, 2) == 3
        assert calc.divide(5, 2) == 2.5
        assert calc.divide(-6, 2) == -3
    
    def test_divide_by_zero(self):
        """Test division by zero raises error"""
        calc = Calculator()
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            calc.divide(5, 0)


class TestEndpoints:
    """Test Flask endpoints"""
    
    def test_home(self, client):
        """Test home endpoint"""
        response = client.get('/')
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'success'
        assert 'version' in data
    
    def test_health(self, client):
        """Test health endpoint"""
        response = client.get('/health')
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'healthy'
    
    def test_calculate_add(self, client):
        """Test calculate endpoint - addition"""
        response = client.post('/calculate', json={
            'operation': 'add',
            'a': 10,
            'b': 5
        })
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'success'
        assert data['result'] == 15
    
    def test_calculate_divide(self, client):
        """Test calculate endpoint - division"""
        response = client.post('/calculate', json={
            'operation': 'divide',
            'a': 10,
            'b': 2
        })
        assert response.status_code == 200
        data = response.get_json()
        assert data['result'] == 5
    
    def test_calculate_divide_by_zero(self, client):
        """Test calculate endpoint - division by zero"""
        response = client.post('/calculate', json={
            'operation': 'divide',
            'a': 10,
            'b': 0
        })
        assert response.status_code == 400
        data = response.get_json()
        assert data['status'] == 'error'
    
    def test_calculate_invalid_operation(self, client):
        """Test calculate endpoint - invalid operation"""
        response = client.post('/calculate', json={
            'operation': 'invalid',
            'a': 10,
            'b': 5
        })
        assert response.status_code == 400
        data = response.get_json()
        assert data['status'] == 'error'
