from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, Union
from .calculations import tvm

app = FastAPI(
    title="Financial Calculator API",
    description="Backend API for Financial Calculator inspired by HP 17BII+",
    version="1.0.0"
)

# Base models
class FinancialFunctionInput(BaseModel):
    """Base model for financial function inputs"""
    pass

class CalculationResult(BaseModel):
    """Base model for calculation results"""
    value: float
    message: Optional[str] = None

# TVM (Time Value of Money) input model
class TVMInput(FinancialFunctionInput):
    n: Optional[float] = Field(None, description="Number of periods")
    i: Optional[float] = Field(None, description="Annual interest rate (as percentage)")
    pv: Optional[float] = Field(None, description="Present value")
    pmt: Optional[float] = Field(None, description="Payment amount")
    fv: Optional[float] = Field(None, description="Future value")
    pyr: int = Field(12, description="Payments per year", ge=1)
    end: bool = Field(True, description="True for end-of-period payments, False for beginning")

    def get_payment_type(self) -> int:
        """Convert end/begin boolean to payment type integer"""
        return 0 if self.end else 1

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"status": "ok", "message": "Financial Calculator API is running"}

@app.get("/api/version")
async def get_version():
    """Get API version information"""
    return {
        "version": "1.0.0",
        "name": "Financial Calculator API",
        "status": "development"
    }

# TVM Endpoints

@app.post("/api/fin/tvm/pv", response_model=CalculationResult)
async def calculate_present_value(input_data: TVMInput):
    """Calculate Present Value (PV) given other TVM parameters"""
    try:
        if input_data.fv is None:
            raise HTTPException(status_code=400, detail="Future value (FV) is required")
        if input_data.i is None:
            raise HTTPException(status_code=400, detail="Interest rate (I%) is required")
        if input_data.n is None:
            raise HTTPException(status_code=400, detail="Number of periods (N) is required")

        pv = tvm.calculate_present_value(
            fv=input_data.fv,
            rate=input_data.i,
            nper=input_data.n,
            pmt=input_data.pmt or 0,
            pmt_type=input_data.get_payment_type()
        )
        
        return CalculationResult(
            value=pv,
            message="Present Value calculated successfully"
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/fin/tvm/fv", response_model=CalculationResult)
async def calculate_future_value(input_data: TVMInput):
    """Calculate Future Value (FV) given other TVM parameters"""
    try:
        if input_data.pv is None:
            raise HTTPException(status_code=400, detail="Present value (PV) is required")
        if input_data.i is None:
            raise HTTPException(status_code=400, detail="Interest rate (I%) is required")
        if input_data.n is None:
            raise HTTPException(status_code=400, detail="Number of periods (N) is required")

        fv = tvm.calculate_future_value(
            pv=input_data.pv,
            rate=input_data.i,
            nper=input_data.n,
            pmt=input_data.pmt or 0,
            pmt_type=input_data.get_payment_type()
        )
        
        return CalculationResult(
            value=fv,
            message="Future Value calculated successfully"
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/fin/tvm/pmt", response_model=CalculationResult)
async def calculate_payment(input_data: TVMInput):
    """Calculate Payment (PMT) given other TVM parameters"""
    try:
        if input_data.pv is None:
            raise HTTPException(status_code=400, detail="Present value (PV) is required")
        if input_data.fv is None:
            raise HTTPException(status_code=400, detail="Future value (FV) is required")
        if input_data.i is None:
            raise HTTPException(status_code=400, detail="Interest rate (I%) is required")
        if input_data.n is None:
            raise HTTPException(status_code=400, detail="Number of periods (N) is required")

        pmt = tvm.calculate_payment(
            pv=input_data.pv,
            fv=input_data.fv,
            rate=input_data.i,
            nper=input_data.n,
            pmt_type=input_data.get_payment_type()
        )
        
        return CalculationResult(
            value=pmt,
            message="Payment amount calculated successfully"
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/fin/tvm/n", response_model=CalculationResult)
async def calculate_periods(input_data: TVMInput):
    """Calculate Number of Periods (N) given other TVM parameters"""
    try:
        if input_data.pv is None:
            raise HTTPException(status_code=400, detail="Present value (PV) is required")
        if input_data.fv is None:
            raise HTTPException(status_code=400, detail="Future value (FV) is required")
        if input_data.i is None:
            raise HTTPException(status_code=400, detail="Interest rate (I%) is required")

        n = tvm.calculate_number_of_periods(
            pv=input_data.pv,
            fv=input_data.fv,
            rate=input_data.i,
            pmt=input_data.pmt or 0,
            pmt_type=input_data.get_payment_type()
        )
        
        return CalculationResult(
            value=n,
            message="Number of periods calculated successfully"
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/fin/tvm/i", response_model=CalculationResult)
async def calculate_interest_rate(input_data: TVMInput):
    """Calculate Interest Rate (I%YR) given other TVM parameters"""
    try:
        if input_data.pv is None:
            raise HTTPException(status_code=400, detail="Present value (PV) is required")
        if input_data.fv is None:
            raise HTTPException(status_code=400, detail="Future value (FV) is required")
        if input_data.n is None:
            raise HTTPException(status_code=400, detail="Number of periods (N) is required")

        i = tvm.calculate_interest_rate(
            pv=input_data.pv,
            fv=input_data.fv,
            nper=input_data.n,
            pmt=input_data.pmt or 0,
            pmt_type=input_data.get_payment_type()
        )
        
        return CalculationResult(
            value=i,
            message="Interest rate calculated successfully"
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))