# Financial Calculator Backend API

FastAPI backend for the Financial Calculator project, providing financial calculation endpoints inspired by the HP 17BII+ calculator.

## Setup

1. Create and activate virtual environment:
```bash
python3 -m venv env
source env/bin/activate  # On Windows: .\env\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Server

Start the development server:
```bash
uvicorn app.main:app --reload
```

The API will be available at http://localhost:8000

## API Documentation

Once the server is running, view the interactive API documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

### Health Check
- GET `/`: Check if API is running

### Version Info
- GET `/api/version`: Get API version information

### TVM (Time Value of Money)
- POST `/api/fin/tvm/pv`: Calculate Present Value
- More endpoints coming soon...

## Development

The API is structured to support various financial calculations:
- TVM (Time Value of Money)
- Interest Rate Conversions
- Cash Flow Analysis
- Bond Calculations
- Depreciation
- Business Schedules

Each category will have its own set of endpoints and Pydantic models for input validation.