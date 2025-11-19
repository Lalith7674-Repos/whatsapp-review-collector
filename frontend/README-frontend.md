# Frontend - WhatsApp Review Collector

React frontend for displaying product reviews collected via WhatsApp.

## Quick Start

1. Install dependencies:
```bash
npm install
```

2. Start development server:
```bash
npm run dev
```

The app will run on `http://localhost:3000`

3. Build for production:
```bash
npm run build
```

## Features

- Fetches reviews from `/api/reviews` endpoint
- Displays reviews in a clean, responsive table
- Auto-refresh functionality
- Error handling with retry option
- Loading states
- Responsive design for mobile devices

## Project Structure

```
frontend/
├── src/
│   ├── App.jsx              # Main application component
│   ├── index.jsx            # React entry point
│   ├── components/
│   │   └── ReviewsTable.jsx  # Table component for reviews
│   └── styles/
│       └── table.css        # Styling
├── index.html               # HTML template
├── vite.config.js           # Vite configuration
└── package.json             # Dependencies
```

## API Integration

The frontend expects the backend to be running on `http://localhost:8000` (configured in `vite.config.js` proxy settings).

The `/api/reviews` endpoint should return a JSON array of review objects with the following structure:

```json
[
  {
    "id": 1,
    "contact_number": "+1234567890",
    "user_name": "John Doe",
    "product_name": "Widget X",
    "product_review": "Great product!",
    "created_at": "2025-01-17T12:34:56Z"
  }
]
```

## Development

- Uses Vite for fast development
- Hot module replacement (HMR) enabled
- Proxy configured to forward `/api/*` requests to backend

