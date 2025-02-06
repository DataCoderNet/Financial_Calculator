"""
Tests for Interest Conversion (ICNV) calculations and endpoints
"""

import pytest
from app.calculations import icnv

def test_nominal_to_effective_annual():
    """Test nominal to effective rate conversion with annual compounding"""
    # 6% nominal rate compounded annually should be 6% effective
    result = icnv.nominal_to_effective(nominal_rate=6.0, compounding_periods=1)
    assert round(result, 4) == 6.0000, "Annual compounding should match nominal rate"

def test_nominal_to_effective_semiannual():
    """Test nominal to effective rate conversion with semi-annual compounding"""
    # 6% nominal rate compounded semi-annually
    # Formula: (1 + 0.06/2)^2 - 1 = 0.0609 or 6.09%
    result = icnv.nominal_to_effective(nominal_rate=6.0, compounding_periods=2)
    assert round(result, 4) == 6.0900, "Semi-annual compounding calculation incorrect"

def test_nominal_to_effective_quarterly():
    """Test nominal to effective rate conversion with quarterly compounding"""
    # 6% nominal rate compounded quarterly
    # Formula: (1 + 0.06/4)^4 - 1 = 0.06136 or 6.136%
    result = icnv.nominal_to_effective(nominal_rate=6.0, compounding_periods=4)
    assert round(result, 4) == 6.1364, "Quarterly compounding calculation incorrect"

def test_nominal_to_effective_monthly():
    """Test nominal to effective rate conversion with monthly compounding"""
    # 6% nominal rate compounded monthly
    # Formula: (1 + 0.06/12)^12 - 1 = 0.0616 or 6.16%
    result = icnv.nominal_to_effective(nominal_rate=6.0, compounding_periods=12)
    assert round(result, 4) == 6.1678, "Monthly compounding calculation incorrect"

def test_effective_to_nominal_annual():
    """Test effective to nominal rate conversion with annual compounding"""
    # 6% effective rate with annual compounding should be 6% nominal
    result = icnv.effective_to_nominal(effective_rate=6.0, compounding_periods=1)
    assert round(result, 4) == 6.0000, "Annual compounding should match effective rate"

def test_effective_to_nominal_semiannual():
    """Test effective to nominal rate conversion with semi-annual compounding"""
    # 6.09% effective rate should give approximately 6% nominal rate with semi-annual compounding
    result = icnv.effective_to_nominal(effective_rate=6.09, compounding_periods=2)
    assert round(result, 4) == 6.0000, "Semi-annual compounding calculation incorrect"

def test_effective_to_nominal_quarterly():
    """Test effective to nominal rate conversion with quarterly compounding"""
    # 6.136% effective rate should give approximately 6% nominal rate with quarterly compounding
    result = icnv.effective_to_nominal(effective_rate=6.1364, compounding_periods=4)
    assert round(result, 4) == 6.0000, "Quarterly compounding calculation incorrect"

def test_effective_to_nominal_monthly():
    """Test effective to nominal rate conversion with monthly compounding"""
    # 6.168% effective rate should give approximately 6% nominal rate with monthly compounding
    result = icnv.effective_to_nominal(effective_rate=6.1678, compounding_periods=12)
    assert round(result, 4) == 6.0000, "Monthly compounding calculation incorrect"

def test_invalid_inputs():
    """Test error handling for invalid inputs"""
    # Test negative nominal rate
    with pytest.raises(ValueError):
        icnv.nominal_to_effective(nominal_rate=-6.0, compounding_periods=12)
    
    # Test negative effective rate
    with pytest.raises(ValueError):
        icnv.effective_to_nominal(effective_rate=-6.0, compounding_periods=12)
    
    # Test zero compounding periods
    with pytest.raises(ValueError):
        icnv.nominal_to_effective(nominal_rate=6.0, compounding_periods=0)

    # Test negative compounding periods
    with pytest.raises(ValueError):
        icnv.effective_to_nominal(effective_rate=6.0, compounding_periods=-1)

def test_api_nominal_to_effective(client):
    """Test the nominal to effective API endpoint"""
    response = client.post(
        "/api/fin/icnv/nominal-to-effective",
        json={"rate": 6.0, "compounding_periods": 12}
    )
    assert response.status_code == 200
    result = response.json()
    assert round(result["value"], 4) == 6.1678

def test_api_effective_to_nominal(client):
    """Test the effective to nominal API endpoint"""
    response = client.post(
        "/api/fin/icnv/effective-to-nominal",
        json={"rate": 6.1678, "compounding_periods": 12}
    )
    assert response.status_code == 200
    result = response.json()
    assert round(result["value"], 4) == 6.0000

def test_api_invalid_inputs(client):
    """Test API error handling for invalid inputs"""
    # Test negative rate
    response = client.post(
        "/api/fin/icnv/nominal-to-effective",
        json={"rate": -6.0, "compounding_periods": 12}
    )
    assert response.status_code == 400

    # Test invalid compounding periods
    response = client.post(
        "/api/fin/icnv/effective-to-nominal",
        json={"rate": 6.0, "compounding_periods": 0}
    )
    assert response.status_code == 400