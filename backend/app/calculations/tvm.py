"""Time Value of Money (TVM) calculations module"""

import numpy_financial as npf
from typing import Optional

def calculate_present_value(
    fv: float,
    rate: float,
    nper: int,
    pmt: float = 0,
    pmt_type: int = 0
) -> float:
    """
    Calculate Present Value (PV)
    
    Parameters:
    - fv: Future value
    - rate: Interest rate (as decimal, e.g., 0.05 for 5%)
    - nper: Number of periods
    - pmt: Payment amount (default: 0)
    - pmt_type: When payments are made (0: end of period [default], 1: beginning of period)
    
    Returns:
    - Present Value (PV)
    """
    try:
        pv = npf.pv(rate=rate/100, nper=nper, pmt=pmt, fv=fv, when=pmt_type)
        return float(-pv)  # Negate to follow cash flow convention
    except Exception as e:
        raise ValueError(f"Error calculating Present Value: {str(e)}")

def calculate_future_value(
    pv: float,
    rate: float,
    nper: int,
    pmt: float = 0,
    pmt_type: int = 0
) -> float:
    """
    Calculate Future Value (FV)
    
    Parameters:
    - pv: Present value
    - rate: Interest rate (as decimal, e.g., 0.05 for 5%)
    - nper: Number of periods
    - pmt: Payment amount (default: 0)
    - pmt_type: When payments are made (0: end of period [default], 1: beginning of period)
    
    Returns:
    - Future Value (FV)
    """
    try:
        fv = npf.fv(rate=rate/100, nper=nper, pmt=pmt, pv=-pv, when=pmt_type)
        return float(fv)  # Convert to float for JSON serialization
    except Exception as e:
        raise ValueError(f"Error calculating Future Value: {str(e)}")

def calculate_payment(
    pv: float,
    fv: float,
    rate: float,
    nper: int,
    pmt_type: int = 0
) -> float:
    """
    Calculate Payment Amount (PMT)
    
    Parameters:
    - pv: Present value
    - fv: Future value
    - rate: Interest rate (as decimal, e.g., 0.05 for 5%)
    - nper: Number of periods
    - pmt_type: When payments are made (0: end of period [default], 1: beginning of period)
    
    Returns:
    - Payment Amount (PMT)
    """
    try:
        pmt = npf.pmt(rate=rate/100, nper=nper, pv=-pv, fv=fv, when=pmt_type)
        return float(pmt)
    except Exception as e:
        raise ValueError(f"Error calculating Payment: {str(e)}")

def calculate_number_of_periods(
    pv: float,
    fv: float,
    rate: float,
    pmt: float = 0,
    pmt_type: int = 0
) -> float:
    """
    Calculate Number of Periods (N)
    
    Parameters:
    - pv: Present value
    - fv: Future value
    - rate: Interest rate (as decimal, e.g., 0.05 for 5%)
    - pmt: Payment amount (default: 0)
    - pmt_type: When payments are made (0: end of period [default], 1: beginning of period)
    
    Returns:
    - Number of Periods (N)
    """
    try:
        nper = npf.nper(rate=rate/100, pmt=pmt, pv=-pv, fv=fv, when=pmt_type)
        return float(nper)
    except Exception as e:
        raise ValueError(f"Error calculating Number of Periods: {str(e)}")

def calculate_interest_rate(
    pv: float,
    fv: float,
    nper: int,
    pmt: float = 0,
    pmt_type: int = 0
) -> float:
    """
    Calculate Interest Rate (I%YR)
    
    Parameters:
    - pv: Present value
    - fv: Future value
    - nper: Number of periods
    - pmt: Payment amount (default: 0)
    - pmt_type: When payments are made (0: end of period [default], 1: beginning of period)
    
    Returns:
    - Interest Rate as percentage
    """
    try:
        rate = npf.rate(nper=nper, pmt=pmt, pv=-pv, fv=fv, when=pmt_type)
        return float(rate * 100)  # Convert to percentage
    except Exception as e:
        raise ValueError(f"Error calculating Interest Rate: {str(e)}")