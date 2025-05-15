from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_add_operation():
    response = client.post(
        "/calculate",
        json={"operand1": 5, "operand2": 3, "operation": "add"}
    )
    assert response.status_code == 200
    assert response.json()["result"] == 8

def test_subtract_operation():
    response = client.post(
        "/calculate",
        json={"operand1": 5, "operand2": 3, "operation": "subtract"}
    )
    assert response.status_code == 200
    assert response.json()["result"] == 2

def test_multiply_operation():
    response = client.post(
        "/calculate",
        json={"operand1": 5, "operand2": 3, "operation": "multiply"}
    )
    assert response.status_code == 200
    assert response.json()["result"] == 15

def test_divide_operation():
    response = client.post(
        "/calculate",
        json={"operand1": 6, "operand2": 3, "operation": "divide"}
    )
    assert response.status_code == 200
    assert response.json()["result"] == 2

def test_divide_by_zero():
    response = client.post(
        "/calculate",
        json={"operand1": 5, "operand2": 0, "operation": "divide"}
    )
    assert response.status_code == 400
    assert "Division by zero is not allowed" in response.json()["detail"]

def test_invalid_operation():
    response = client.post(
        "/calculate",
        json={"operand1": 5, "operand2": 3, "operation": "invalid"}
    )
    assert response.status_code == 400
    assert "Invalid operation" in response.json()["detail"]

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"