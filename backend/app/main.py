from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional
from .calculations import tvm, icnv

app = FastAPI(
    title="Financial Calculator API",
    description="Backend API for Financial Calculator inspired by HP 17BII+",
    version="1.0.0"
)

# Configure CORS
origins = [
    "http://localhost:5173",  # Vite default
    "http://localhost:5174",  # Vite alternate
    "http://127.0.0.1:5173",
    "http://127.0.0.1:5174",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class ICNVInput(BaseModel):
    rate: float = Field(..., description="Interest rate (as percentage)")
    compounding_periods: int = Field(..., description="Number of compounding periods per year", ge=1)

class TVMInput(BaseModel):
    n: Optional[float] = Field(None, description="Number of periods")
    i: Optional[float] = Field(None, description="Annual interest rate (as percentage)")
    pv: Optional[float] = Field(None, description="Present value")
    pmt: Optional[float] = Field(None, description="Payment amount")
    fv: Optional[float] = Field(None, description="Future value")
    pyr: int = Field(12, description="Payments per year", ge=1)
    end: bool = Field(True, description="True for end-of-period payments, False for beginning")

    def get_payment_type(self) -> int:
        return 0 if self.end else 1

class CalculationResult(BaseModel):
    value: float
    message: Optional[str] = None

@app.get("/")
async def root():
    return {"status": "ok", "message": "Financial Calculator API is running"}

# TVM Endpoints
@app.post("/api/fin/tvm/pv")
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
        
        return {"value": pv}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/fin/tvm/fv")
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
        
        return {"value": fv}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/fin/tvm/n")
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
        
        return {"value": n}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/fin/tvm/i")
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
        
        return {"value": i}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/fin/tvm/pmt")
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
        
        return {"value": pmt}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# ICNV Endpoints
@app.post("/api/fin/icnv/nominal-to-effective")
async def convert_nominal_to_effective(input_data: ICNVInput):
    """Convert nominal interest rate to effective annual rate"""
    try:
        effective_rate = icnv.nominal_to_effective(
            nominal_rate=input_data.rate,
            compounding_periods=input_data.compounding_periods
        )
        return {"value": effective_rate}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/fin/icnv/effective-to-nominal")
async def convert_effective_to_nominal(input_data: ICNVInput):
    """Convert effective annual rate to nominal interest rate"""
    try:
        nominal_rate = icnv.effective_to_nominal(
            effective_rate=input_data.rate,
            compounding_periods=input_data.compounding_periods
        )
        return {"value": nominal_rate}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))