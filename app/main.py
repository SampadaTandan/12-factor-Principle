from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from enum import Enum
from typing import Optional

app = FastAPI(
    title="Calculator API",
    description="A simple calculator microservice with RESTful endpoints",
    version="1.0.0",
    openapi_tags=[{
        "name": "calculations",
        "description": "Arithmetic operations endpoints"
    }, {
        "name": "health",
        "description": "Health check endpoints"
    }]
)

class Operation(str, Enum):
    ADD = "add"
    SUBTRACT = "subtract"
    MULTIPLY = "multiply"
    DIVIDE = "divide"

class CalculationRequest(BaseModel):
    number1: float = Query(..., description="First operand", example=10.5)
    number2: float = Query(..., description="Second operand", example=5.2)
    operation: Operation = Query(..., description="Arithmetic operation to perform")

class CalculationResponse(BaseModel):
    result: float = Query(..., description="The calculation result")
    detail: str = Query(..., description="Human-readable operation detail")
    operation: str = Query(..., description="Type of operation performed")

@app.get("/health", tags=["health"])
async def health_check():
    """Service health check endpoint"""
    return {"status": "healthy", "service": "calculator-api"}

@app.post("/calculate", 
          response_model=CalculationResponse, 
          tags=["calculations"],
          summary="Perform arithmetic calculation",
          responses={
              200: {"description": "Successful calculation"},
              400: {"description": "Invalid input or operation"}
          })
async def calculate(request: CalculationRequest):
    """
    Perform arithmetic calculations with two numbers.
    
    Supports the following operations:
    - add (+)
    - subtract (-)
    - multiply (*)
    - divide (/)
    """
    try:
        operation_detail = {
            Operation.ADD: ("+", request.number1 + request.number2),
            Operation.SUBTRACT: ("-", request.number1 - request.number2),
            Operation.MULTIPLY: ("*", request.number1 * request.number2),
            Operation.DIVIDE: ("/", request.number1 / request.number2 
                              if request.number2 != 0 
                              else None)
        }
        
        if request.operation == Operation.DIVIDE and request.number2 == 0:
            raise HTTPException(status_code=400, detail="Cannot divide by zero")
            
        operator, result = operation_detail[request.operation]
        detail = f"{request.number1} {operator} {request.number2}"
        
        return CalculationResponse(
            result=result,
            detail=detail,
            operation=request.operation.value
        )
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/add", 
         response_model=CalculationResponse, 
         tags=["calculations"],
         summary="Add two numbers")
async def add(
    number1: float = Query(..., example=10.5),
    number2: float = Query(..., example=5.2)
):
    """Add two numbers together"""
    result = number1 + number2
    return CalculationResponse(
        result=result,
        detail=f"{number1} + {number2}",
        operation="add"
    )

@app.get("/subtract", 
         response_model=CalculationResponse, 
         tags=["calculations"],
         summary="Subtract two numbers")
async def subtract(
    number1: float = Query(..., example=15.0),
    number2: float = Query(..., example=7.5)
):
    """Subtract the second number from the first"""
    result = number1 - number2
    return CalculationResponse(
        result=result,
        detail=f"{number1} - {number2}",
        operation="subtract"
    )

@app.get("/multiply", 
         response_model=CalculationResponse, 
         tags=["calculations"],
         summary="Multiply two numbers")
async def multiply(
    number1: float = Query(..., example=8.0),
    number2: float = Query(..., example=3.5)
):
    """Multiply two numbers together"""
    result = number1 * number2
    return CalculationResponse(
        result=result,
        detail=f"{number1} * {number2}",
        operation="multiply"
    )

@app.get("/divide", 
         response_model=CalculationResponse, 
         tags=["calculations"],
         summary="Divide two numbers",
         responses={
             200: {"description": "Successful division"},
             400: {"description": "Division by zero attempted"}
         })
async def divide(
    number1: float = Query(..., example=20.0),
    number2: float = Query(..., example=4.0)
):
    """Divide the first number by the second"""
    if number2 == 0:
        raise HTTPException(status_code=400, detail="Cannot divide by zero")
    
    result = number1 / number2
    return CalculationResponse(
        result=result,
        detail=f"{number1} / {number2}",
        operation="divide"
    )