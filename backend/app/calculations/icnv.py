"""Interest Conversion calculations module"""

def nominal_to_effective(
    nominal_rate: float,
    compounding_periods: int
) -> float:
    """
    Convert nominal rate to effective annual rate
    
    Parameters:
    - nominal_rate: Nominal annual rate (as percentage)
    - compounding_periods: Number of compounding periods per year
    
    Returns:
    - Effective annual rate (as percentage)
    
    Formula: effective_rate = (1 + nominal_rate/(100*m))^m - 1
    where m is the number of compounding periods per year
    """
    try:
        if nominal_rate <= 0:
            raise ValueError("Nominal rate must be positive")
        if compounding_periods <= 0:
            raise ValueError("Number of compounding periods must be positive")
            
        nominal_decimal = nominal_rate / 100
        rate_per_period = nominal_decimal / compounding_periods
        effective_rate = (1 + rate_per_period) ** compounding_periods - 1
        return float(effective_rate * 100)  # Convert back to percentage
    except Exception as e:
        raise ValueError(f"Error calculating effective rate: {str(e)}")

def effective_to_nominal(
    effective_rate: float,
    compounding_periods: int
) -> float:
    """
    Convert effective annual rate to nominal rate
    
    Parameters:
    - effective_rate: Effective annual rate (as percentage)
    - compounding_periods: Number of compounding periods per year
    
    Returns:
    - Nominal annual rate (as percentage)
    
    Formula: nominal_rate = m * ((1 + effective_rate/100)^(1/m) - 1)
    where m is the number of compounding periods per year
    """
    try:
        if effective_rate <= 0:
            raise ValueError("Effective rate must be positive")
        if compounding_periods <= 0:
            raise ValueError("Number of compounding periods must be positive")
            
        effective_decimal = effective_rate / 100
        rate_per_period = ((1 + effective_decimal) ** (1/compounding_periods) - 1)
        nominal_rate = rate_per_period * compounding_periods
        return float(nominal_rate * 100)  # Convert back to percentage
    except Exception as e:
        raise ValueError(f"Error calculating nominal rate: {str(e)}")