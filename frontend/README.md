# Blood Parameter Analysis - Frontend

React + TypeScript frontend for blood parameter analysis with Flask backend integration. Features AI-powered disease risk prediction, blood report OCR, and personalized health recommendations.

## Features

- 🔐 **User Authentication** - Secure login/signup with JWT tokens
- 📄 **Blood Report Upload** - OCR processing of PDF/Image reports  
- 🧪 **Manual Parameter Entry** - Form-based blood parameter input
- 🤖 **ML Analysis** - AI-powered disease risk prediction via Flask API
- 📊 **Visual Results** - Interactive charts and risk assessments
- 📈 **History Tracking** - View and compare past analyses
- 🌍 **Multi-language** - Support for multiple languages

## Prerequisites

- Node.js 18+ and npm
- Your Flask backend API running (see [FLASK_API_INTEGRATION.md](./FLASK_API_INTEGRATION.md))

## Quick Start

1. **Install dependencies:**
```bash
npm install
```

2. **Configure API endpoint:**
```bash
cp .env.example .env
```

Edit `.env` and set your Flask API URL:
```
VITE_API_URL=http://localhost:5000/api
```

3. **Start development server:**
```bash
npm run dev
```

The app will run at `http://localhost:8080`

## Flask Backend Integration

This frontend requires a Flask backend. See **[FLASK_API_INTEGRATION.md](./FLASK_API_INTEGRATION.md)** for:
- ✅ Required API endpoints with request/response formats
- ✅ Database schema recommendations (Oracle SQL compatible)
- ✅ Authentication flow (JWT-based)
- ✅ CORS configuration
- ✅ Error handling guidelines

## Project Structure

```
src/
├── assets/              # Images and static files
├── components/          
│   ├── auth/           # Login/Signup forms
│   ├── dashboard/      # Upload & parameter input
│   ├── results/        # Analysis results display
│   └── ui/             # Reusable UI components (shadcn)
├── config/             
│   └── api.js          # API endpoint configuration
├── hooks/              # Custom React hooks
├── pages/              
│   ├── Login.tsx       # Login page
│   ├── Signup.tsx      # Signup page
│   ├── Dashboard.tsx   # Main dashboard
│   ├── Results.tsx     # Analysis results
│   ├── History.tsx     # Report history
│   └── About.tsx       # About page
├── services/           
│   └── api.js          # API client (connect to Flask here)
└── utils/              # Utility functions
```

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build

## Connecting Your Flask Backend

### 1. Implement Required Endpoints

Your Flask API must implement these endpoints (see [FLASK_API_INTEGRATION.md](./FLASK_API_INTEGRATION.md)):

- `POST /auth/signup` - User registration
- `POST /auth/login` - User login (returns JWT)
- `POST /auth/logout` - User logout
- `GET /auth/user` - Get current user
- `POST /reports/upload` - Upload blood report for OCR
- `POST /reports/analyze` - Analyze parameters with ML model
- `GET /reports/history` - Get user's report history
- `GET /reports/{id}` - Get specific report
- `GET /parameters` - Get blood parameter definitions

### 2. Enable CORS in Flask

```python
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=['http://localhost:8080'])
```

### 3. Update Configuration

Edit `src/config/api.js` if your Flask URL differs:

```javascript
export const API_BASE_URL = 'http://your-flask-url:5000/api';
```

## Authentication Flow

1. User signs up/logs in → Flask returns JWT token
2. Frontend stores token in `localStorage`
3. All API requests include token in `Authorization: Bearer {token}` header
4. Flask validates token and returns data

## ML Model Integration

Your Flask backend should:
- Accept blood parameters via `/reports/analyze`
- Run ML models for disease prediction
- Return risk scores, disease probabilities, and recommendations
- Store results in your Oracle database

Example response structure:
```json
{
  "report_id": "uuid",
  "analysis": {
    "overall_risk": "low",
    "risk_score": 25,
    "disease_risks": [...],
    "recommendations": [...]
  }
}
```

## Tech Stack

- **React 18** - UI framework
- **TypeScript** - Type safety
- **Vite** - Build tool & dev server
- **Tailwind CSS** - Styling
- **shadcn/ui** - Component library
- **React Router** - Navigation
- **Lucide React** - Icons

## Development

The frontend is completely independent of backend implementation. You can:
- Use any database (Oracle, PostgreSQL, etc.)
- Implement ML models in Python (scikit-learn, TensorFlow, etc.)
- Deploy separately from the backend

Just ensure your Flask API implements the required endpoints!

## Building for Production

```bash
npm run build
```

This creates a `dist/` folder with optimized static files ready for deployment.

## Deployment

Deploy the `dist/` folder to:
- Netlify
- Vercel
- AWS S3 + CloudFront
- Any static hosting service

Make sure to set the `VITE_API_URL` environment variable to your production Flask API URL.

## License

MIT
