# Fantasy Football Analysis Platform

A comprehensive fantasy football analysis platform with a Django REST API backend and React TypeScript frontend. Analyze your league's performance, draft strategies, and get advanced insights into luck, consistency, and expected wins.

## 🏈 Features

### Core Analysis
- **Expected Wins Analysis** - Compare actual vs expected wins
- **Luck Analysis** - Statistical analysis of team luck
- **Consistency Metrics** - Team performance consistency analysis
- **Bonage Index** - Strength of schedule analysis
- **Probability Curves** - Statistical probability distributions

### Draft Analysis
- **Sleepers Analysis** - Identify draft steals and busts
- **Positional Rank Tracking** - Track draft position vs performance
- **Draft Injury Analysis** - Injury impact on draft picks
- **Draft Round Analysis** - Performance by draft round

### Platform Support
- **ESPN Fantasy Football** - Full integration with authentication
- **Sleeper Fantasy Football** - Complete platform support
- **Real-time Progress** - Live assembly progress tracking
- **Caching System** - Efficient data caching for performance

## 🏗️ Architecture

### Backend (Django)
- **Django REST Framework** - RESTful API endpoints
- **League Assembly** - Heavy processing separated from light analysis
- **Caching System** - Redis-based caching for league objects
- **Server-Sent Events** - Real-time progress streaming
- **Draft Processing** - Separate draft analysis workflow

### Frontend (React)
- **React 18** with TypeScript
- **Vite** for fast development
- **Tailwind CSS** for styling
- **React Query** for server state management
- **Plotly.js** for interactive charts
- **Real-time Progress** - Live assembly progress display

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 18+
- Redis (for caching)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd mysite
   ```

2. **Install all dependencies**
   ```bash
   npm run install:all
   ```

3. **Setup the backend**
   ```bash
   npm run setup
   ```

4. **Start both servers**
   ```bash
   npm run dev
   ```

This will start:
- Django backend at `http://127.0.0.1:8000`
- React frontend at `http://localhost:5173`

## 📁 Project Structure

```
mysite/
├── analysis/              # Django app with core analysis logic
│   ├── league/           # League processing and analysis
│   ├── api_views.py      # REST API endpoints
│   ├── api_urls.py       # API URL routing
│   └── analysisfuncs.py  # Analysis functions
├── fantasy/              # Django project settings
│   ├── settings.py       # Django settings
│   ├── urls.py          # Main URL routing
│   └── wsgi.py          # WSGI configuration
├── frontend/            # React frontend
│   ├── src/
│   │   ├── components/  # React components
│   │   ├── hooks/      # Custom hooks
│   │   ├── pages/      # Page components
│   │   ├── services/   # API services
│   │   └── utils/      # Utilities
│   └── package.json
├── manage.py            # Django management script
├── package.json         # Root package.json
└── README.md
```

## 🔧 Development

### Backend Development

The Django backend provides a REST API with the following key features:

#### Assembly Endpoints
- `POST /api/v1/leagues/assemble-scoring/` - Assemble league scoring data
- `POST /api/v1/leagues/assemble-draft/` - Assemble league draft data
- `POST /api/v1/leagues/assemble-scoring-stream/` - Streaming assembly with progress

#### Analysis Endpoints
- `GET /api/v1/leagues/{id}/scoring/expected-wins/` - Expected wins analysis
- `GET /api/v1/leagues/{id}/scoring/ew-difference/` - EW difference analysis
- `GET /api/v1/leagues/{id}/scoring/luck/` - Luck analysis
- `GET /api/v1/leagues/{id}/scoring/bonage/` - Bonage analysis
- `GET /api/v1/leagues/{id}/scoring/consistency/` - Consistency analysis
- `GET /api/v1/leagues/{id}/scoring/probability-curve/` - Probability curve
- `GET /api/v1/leagues/{id}/draft/sleepers/` - Sleepers analysis
- `GET /api/v1/leagues/{id}/draft/positional-ranks/` - Positional ranks
- `GET /api/v1/leagues/{id}/draft/injury-table/` - Draft injury table

#### Draft Processing
- `POST /api/v1/leagues/{id}/process-draft/` - Process draft data separately

### Frontend Development

The React frontend provides a modern, responsive interface:

#### Key Features
- **Real-time Progress** - Live assembly progress with Server-Sent Events
- **Interactive Charts** - Plotly.js integration for data visualization
- **Type Safety** - Full TypeScript support
- **State Management** - React Query for server state
- **Responsive Design** - Tailwind CSS for modern styling

#### Development Commands
```bash
cd frontend
npm run dev          # Start development server
npm run build        # Build for production
npm run preview      # Preview production build
```

## 📊 API Documentation

### League Assembly

#### Assemble Scoring Data
```http
POST /api/v1/leagues/assemble-scoring/
Content-Type: application/json

{
  "platform": "espn",
  "league_id": "123456",
  "s2": "your_espn_s2_token",
  "swid": "your_espn_swid"
}
```

#### Assemble Draft Data
```http
POST /api/v1/leagues/assemble-draft/
Content-Type: application/json

{
  "platform": "sleeper",
  "league_id": "789012"
}
```

### Analysis Endpoints

All analysis endpoints return HTML chart code and metadata:

```json
{
  "chart_html": "<div>...</div>",
  "metadata": {
    "league_id": "123456",
    "analysis_type": "expected_wins",
    "num_teams": 12,
    "num_weeks": 14
  }
}
```

## 🎯 Usage Examples

### 1. Setup a League

1. Navigate to the setup page
2. Enter your league credentials (ESPN or Sleeper)
3. Watch real-time progress as the league assembles
4. Access analysis once assembly is complete

### 2. View Analysis

- **Expected Wins** - See how teams performed vs expectations
- **Luck Analysis** - Statistical analysis of team luck
- **Draft Analysis** - Review draft performance and sleepers
- **Consistency** - Team performance consistency metrics

### 3. Draft Processing

For leagues with draft data:
1. Assemble the league normally
2. Process draft data separately (if needed)
3. Access draft-specific analysis

## 🔍 Testing

### Backend Tests
```bash
python manage.py test
```

### Frontend Tests
```bash
cd frontend
npm test
```

### API Testing
Use the provided test scripts:
```bash
python test_api.py
```

## 🚀 Deployment

### Backend Deployment
1. Set up a production Django environment
2. Configure Redis for caching
3. Set environment variables
4. Run migrations

### Frontend Deployment
1. Build the frontend: `npm run build`
2. Serve the `dist/` folder
3. Configure API base URL

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

MIT License - see LICENSE file for details

## 🆘 Support

For issues and questions:
1. Check the documentation
2. Review existing issues
3. Create a new issue with detailed information

---

Built with ❤️ for fantasy football enthusiasts 