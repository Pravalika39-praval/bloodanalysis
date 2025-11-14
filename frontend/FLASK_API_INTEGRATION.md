# Flask API Integration Guide

This frontend expects the following Flask API endpoints. All endpoints should return JSON responses.

## Base URL
Configure your Flask API URL in `src/config/api.js`:
```javascript
export const API_BASE_URL = 'http://localhost:5000/api'; // Change to your Flask URL
```

## Required Flask Endpoints

### 1. Authentication Endpoints

#### POST `/auth/signup`
**Request Body:**
@app.route("/api/auth/signup", methods=["POST"])
```json
{
  "email": "user@example.com",
  "password": "password123",
  "full_name": "John Doe"
}
```
**Response (Success - 201):**
```json
{
  "user": {
    "id": "user_id",
    "email": "user@example.com",
    "full_name": "John Doe"
  },
  "token": "jwt_token_here"
}
```

#### POST `/auth/login`
**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```
**Response (Success - 200):**
```json
{
  "user": {
    "id": "user_id",
    "email": "user@example.com",
    "full_name": "John Doe"
  },
  "token": "jwt_token_here"
}
```

#### POST `/auth/logout`
**Headers:**
```
Authorization: Bearer {token}
```
**Response (Success - 200):**
```json
{
  "message": "Logged out successfully"
}
```

#### GET `/auth/user`
**Headers:**
```
Authorization: Bearer {token}
```
**Response (Success - 200):**
```json
{
  "id": "user_id",
  "email": "user@example.com",
  "full_name": "John Doe"
}
```

### 2. Blood Report Analysis Endpoints

#### POST `/reports/upload`
Upload blood report file (PDF/Image) for OCR processing
**Headers:**
```
Authorization: Bearer {token}
Content-Type: multipart/form-data
```
**Request Body (FormData):**
```
file: [PDF/JPG/PNG file]
```
**Response (Success - 200):**
```json
{
  "report_id": "report_id",
  "extracted_parameters": {
    "hemoglobin": 13.5,
    "wbc": 7200,
    "rbc": 4.8,
    "platelets": 280000,
    "glucose": 95,
    "cholesterol": 185,
    "hdl": 55,
    "ldl": 110,
    "triglycerides": 130,
    "creatinine": 0.9
  }
}
```

#### POST `/reports/analyze`
Analyze blood parameters using ML model
**Headers:**
```
Authorization: Bearer {token}
Content-Type: application/json
```
**Request Body:**
```json
{
  "parameters": {
    "hemoglobin": 13.5,
    "wbc": 7200,
    "rbc": 4.8,
    "platelets": 280000,
    "glucose": 95,
    "cholesterol": 185,
    "hdl": 55,
    "ldl": 110,
    "triglycerides": 130,
    "creatinine": 0.9
  }
}
```
**Response (Success - 200):**
```json
{
  "report_id": "report_id",
  "analysis": {
    "overall_risk": "low",
    "risk_score": 25,
    "disease_risks": [
      {
        "disease": "Diabetes",
        "risk_level": "low",
        "probability": 15,
        "factors": ["Glucose levels normal"]
      },
      {
        "disease": "Cardiovascular Disease",
        "risk_level": "low",
        "probability": 20,
        "factors": ["Cholesterol within range"]
      }
    ],
    "abnormal_parameters": [],
    "recommendations": [
      "Maintain current healthy lifestyle",
      "Regular exercise recommended",
      "Annual check-up advised"
    ]
  },
  "created_at": "2024-01-15T10:30:00Z"
}
```

### 3. History Endpoints

#### GET `/reports/history`
Get user's blood report history
**Headers:**
```
Authorization: Bearer {token}
```
**Response (Success - 200):**
```json
{
  "reports": [
    {
      "id": "report_id",
      "created_at": "2024-01-15T10:30:00Z",
      "overall_risk": "low",
      "risk_score": 25,
      "parameters": {
        "hemoglobin": 13.5,
        "wbc": 7200,
        "glucose": 95
      }
    }
  ]
}
```

#### GET `/reports/{report_id}`
Get specific report details
**Headers:**
```
Authorization: Bearer {token}
```
**Response (Success - 200):**
```json
{
  "id": "report_id",
  "created_at": "2024-01-15T10:30:00Z",
  "parameters": {
    "hemoglobin": 13.5,
    "wbc": 7200,
    "rbc": 4.8,
    "platelets": 280000,
    "glucose": 95,
    "cholesterol": 185,
    "hdl": 55,
    "ldl": 110,
    "triglycerides": 130,
    "creatinine": 0.9
  },
  "analysis": {
    "overall_risk": "low",
    "risk_score": 25,
    "disease_risks": [...],
    "recommendations": [...]
  }
}
```

### 4. Parameter Definitions Endpoint

#### GET `/parameters`
Get blood parameter definitions with normal ranges
**Response (Success - 200):**
```json
{
  "parameters": [
    {
      "id": "hemoglobin",
      "parameter_name": "hemoglobin",
      "display_name": "Hemoglobin",
      "unit": "g/dL",
      "normal_range_min": 12.0,
      "normal_range_max": 16.0,
      "category": "Blood Cells"
    },
    {
      "id": "wbc",
      "parameter_name": "wbc",
      "display_name": "White Blood Cells",
      "unit": "cells/μL",
      "normal_range_min": 4000,
      "normal_range_max": 11000,
      "category": "Blood Cells"
    }
  ]
}
```

## Error Responses

All endpoints should return appropriate error responses:

**401 Unauthorized:**
```json
{
  "error": "Unauthorized",
  "message": "Invalid or expired token"
}
```

**400 Bad Request:**
```json
{
  "error": "Bad Request",
  "message": "Invalid input data"
}
```

**500 Internal Server Error:**
```json
{
  "error": "Internal Server Error",
  "message": "An error occurred processing your request"
}
```

## CORS Configuration

Your Flask API must enable CORS to allow requests from the frontend:

```python
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=['http://localhost:8080'])  # Add your frontend URL
```

## Authentication Flow

1. User signs up/logs in → Flask returns JWT token
2. Frontend stores token in localStorage
3. All subsequent requests include token in Authorization header
4. Flask validates token and returns user data

## Running the Integration

1. Start your Flask backend: `python app.py`
2. Update `src/config/api.js` with your Flask URL
3. Start the frontend: `npm run dev`
4. The frontend will connect to your Flask API automatically
