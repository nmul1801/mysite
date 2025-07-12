# Fantasy Football Analysis Frontend

A modern React frontend for the Fantasy Football Analysis platform, built with TypeScript, Vite, and Tailwind CSS.

## Features

- **Modern React Stack**: Built with React 18, TypeScript, and Vite
- **Beautiful UI**: Styled with Tailwind CSS and custom components
- **Real-time Progress**: Server-Sent Events for live assembly progress
- **Advanced Analytics**: Interactive charts with Plotly.js
- **Type Safety**: Full TypeScript support with proper type definitions
- **State Management**: React Query for server state management
- **Routing**: React Router for navigation
- **Notifications**: Toast notifications with react-hot-toast

## Tech Stack

- **React 18** with TypeScript
- **Vite** for fast development and building
- **Tailwind CSS** for styling
- **React Query** for server state management
- **React Router** for navigation
- **Axios** for API calls
- **Plotly.js** for interactive charts
- **React Hook Form** for form handling
- **Framer Motion** for animations
- **React Hot Toast** for notifications

## Project Structure

```
src/
├── components/          # Reusable UI components
│   ├── Layout/         # Layout components (Header, etc.)
│   ├── ProgressBar/    # Progress tracking components
│   ├── LeagueSelector/ # League selection components
│   └── AnalysisCharts/ # Chart components
├── hooks/              # Custom React hooks
├── pages/              # Page components
├── services/           # API services and types
├── utils/              # Utility functions
└── App.tsx            # Main app component
```

## Getting Started

### Prerequisites

- Node.js 18+ 
- npm or yarn
- Backend Django server running

### Installation

1. Install dependencies:
   ```bash
   npm install
   ```

2. Start the development server:
   ```bash
   npm run dev
   ```

3. Open your browser to `http://localhost:5173`

### Environment Variables

Create a `.env` file in the frontend directory:

```env
VITE_API_BASE_URL=http://127.0.0.1:8000/api/v1
```

## Development

### Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint
- `npm run type-check` - Run TypeScript type checking

### Key Components

#### API Service (`src/services/api.ts`)
Handles all API communication with the Django backend, including:
- League assembly (scoring and draft)
- Progress tracking
- Analysis data fetching
- Draft processing

#### Custom Hooks
- `useLeagueAssembly` - Manages league assembly with progress tracking
- `useAnalysisData` - Fetches and manages analysis data with React Query

#### Components
- `ProgressBar` - Real-time progress display
- `Header` - Navigation and branding
- `Dashboard` - Main landing page

## API Integration

The frontend integrates with the Django REST API endpoints:

### Assembly Endpoints
- `POST /api/v1/leagues/assemble-scoring/` - Assemble league scoring data
- `POST /api/v1/leagues/assemble-draft/` - Assemble league draft data
- `POST /api/v1/leagues/assemble-scoring-stream/` - Streaming assembly with progress

### Analysis Endpoints
- `GET /api/v1/leagues/{id}/scoring/expected-wins/` - Expected wins analysis
- `GET /api/v1/leagues/{id}/scoring/ew-difference/` - EW difference analysis
- `GET /api/v1/leagues/{id}/scoring/luck/` - Luck analysis
- `GET /api/v1/leagues/{id}/draft/sleepers/` - Sleepers analysis
- And many more...

### Progress Tracking
- `GET /api/v1/progress/{id}/` - Get assembly progress

## Styling

The project uses Tailwind CSS with custom components defined in `src/index.css`. Key utility classes:

- `.btn-primary` - Primary button styling
- `.btn-secondary` - Secondary button styling
- `.card` - Card container styling
- `.input-field` - Form input styling

## TypeScript

The project includes comprehensive TypeScript types in `src/services/types.ts`:

- `LeagueAssemblyRequest` - League assembly request data
- `LeagueAssemblyResponse` - Assembly response data
- `AnalysisResponse` - Analysis endpoint responses
- `ProgressUpdate` - Real-time progress updates
- `DebugResponse` - Debug endpoint data

## Building for Production

```bash
npm run build
```

This creates a `dist/` folder with optimized production files.

## Contributing

1. Follow the existing code style
2. Add TypeScript types for new features
3. Use React Query for server state
4. Add proper error handling
5. Test with the Django backend running
