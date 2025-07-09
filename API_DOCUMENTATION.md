# Fantasy Football Analysis API Documentation

## Overview

This API provides fantasy football league analysis with separate endpoints for data assembly and analysis. The architecture separates heavy data processing (league assembly) from light analysis processing for optimal performance.

## Base URL

```
http://127.0.0.1:8000/api/v1/
```

## Architecture

### Data Assembly Endpoints (Heavy Processing)
- **POST** `/leagues/assemble-scoring/` - Assemble league data for scoring analysis
- **POST** `/leagues/assemble-draft/` - Assemble league data for draft analysis

### Analysis Endpoints (Light Processing)

#### Scoring Analysis
- **GET** `/leagues/{league_id}/scoring/expected-wins/`
- **GET** `/leagues/{league_id}/scoring/ew-difference/`
- **GET** `/leagues/{league_id}/scoring/luck/`
- **GET** `/leagues/{league_id}/scoring/bonage/`
- **GET** `/leagues/{league_id}/scoring/consistency/`
- **GET** `/leagues/{league_id}/scoring/probability-curve/`

#### Draft Analysis
- **GET** `/leagues/{league_id}/draft/sleepers/`
- **GET** `/leagues/{league_id}/draft/positional-ranks/`
- **GET** `/leagues/{league_id}/draft/injury-table/`

#### Debug
- **GET** `/leagues/{league_id}/debug/` - Debug league information

## Endpoint Details

### 1. Assemble Scoring League

**POST** `/leagues/assemble-scoring/`

Assembles league data for scoring analysis. This is the heavy processing step that should be called once before making multiple analysis requests.

**Request Body:**
```json
{
  "platform": "espn|sleeper",
  "league_id": "string",
  "s2": "string",        // Required for ESPN
  "swid": "string"       // Required for ESPN
}
```

**Response:**
```json
{
  "league_id": "scoring_123_espn_abc12345",
  "status": "ready"
}
```

**Status Codes:**
- `200` - Successfully assembled
- `400` - Bad request (missing league_id)
- `500` - Server error

**Performance:** 5-10 seconds (heavy processing)

### 2. Assemble Draft League

**POST** `/leagues/assemble-draft/`

Assembles league data for draft analysis. Similar to scoring assembly but optimized for draft-related data.

**Request Body:** Same as scoring assembly

**Response:** Same structure as scoring assembly

**Performance:** 5-10 seconds (heavy processing)

### 3. Expected Wins Analysis

**GET** `/leagues/{league_id}/scoring/expected-wins/`

Returns expected wins analysis chart as HTML.

**Response:**
```json
{
  "chart_html": "<div id='plotly-chart'>...</div>",
  "metadata": {
    "league_id": "scoring_123_espn_abc12345",
    "analysis_type": "expected_wins",
    "chart_type": "bar",
    "num_teams": 10,
    "num_weeks": 12
  }
}
```

**Performance:** < 1 second (light processing)

### 4. Expected Wins Difference Analysis

**GET** `/leagues/{league_id}/scoring/ew-difference/`

Returns expected wins difference analysis with summary data.

**Response:**
```json
{
  "chart_html": "<div id='plotly-chart'>...</div>",
  "metadata": {
    "league_id": "scoring_123_espn_abc12345",
    "analysis_type": "ew_difference",
    "chart_type": "bar",
    "num_teams": 10,
    "num_weeks": 12,
    "summary": {
      "lucky_name": "Team1",
      "l_total_wins": 8.5,
      "l_total_ex_wins": 6.2,
      "l_ew_diff": 2.3,
      "unlucky_name": "Team2",
      "u_total_wins": 3.1,
      "u_total_ex_wins": 5.8,
      "u_ew_diff": 2.7
    }
  }
}
```

**Performance:** < 1 second (light processing)

### 5. Luck Analysis

**GET** `/leagues/{league_id}/scoring/luck/`

Returns luck analysis with probability calculations.

**Response:**
```json
{
  "chart_html": "<div id='plotly-chart'>...</div>",
  "metadata": {
    "league_id": "scoring_123_espn_abc12345",
    "analysis_type": "luck",
    "chart_type": "bar",
    "num_teams": 10,
    "num_weeks": 12,
    "summary": {
      "l_prob": 85.2,
      "u_prob": 15.8,
      "perc_lucky": 84.2
    }
  }
}
```

**Performance:** < 1 second (light processing)

### 6. Bonage Analysis

**GET** `/leagues/{league_id}/scoring/bonage/`

Returns bonage (strength of schedule) analysis.

**Performance:** < 1 second (light processing)

### 7. Consistency Analysis

**GET** `/leagues/{league_id}/scoring/consistency/`

Returns team consistency analysis as scatter plot.

**Performance:** < 1 second (light processing)

### 8. Probability Curve Analysis

**GET** `/leagues/{league_id}/scoring/probability-curve/`

Returns probability distribution curve for luck analysis.

**Performance:** < 1 second (light processing)

### 9. Sleepers Analysis

**GET** `/leagues/{league_id}/draft/sleepers/`

Returns sleeper picks analysis data.

**Response:**
```json
{
  "data": [
    ["QB", "Player Name"],
    ["RB", "Player Name"],
    ...
  ],
  "metadata": {
    "league_id": "draft_123_espn_abc12345",
    "analysis_type": "sleepers",
    "num_teams": 10,
    "num_weeks": 12
  }
}
```

**Performance:** < 1 second (light processing)

### 10. Positional Ranks Analysis

**GET** `/leagues/{league_id}/draft/positional-ranks/`

Returns positional ranking analysis through the draft.

**Performance:** < 1 second (light processing)

### 11. Draft Injury Analysis

**GET** `/leagues/{league_id}/draft/injury-table/`

Returns draft injury analysis data.

**Performance:** < 1 second (light processing)

### 12. Debug League Info

**GET** `/leagues/{league_id}/debug/`

Returns detailed information about the cached league object for debugging.

**Response:**
```json
{
  "num_teams": 10,
  "num_weeks": 12,
  "assembly_type": "scoring",
  "teams": {
    "1": {
      "name": "Team1",
      "has_scores": true,
      "has_wins": true,
      "has_ranks": true,
      "score_count": 12,
      "win_count": 12,
      "rank_count": 12
    }
  }
}
```

**Performance:** < 1 second (light processing)

## Caching Strategy

- **Scoring Assembly**: Cached for 1 hour
- **Draft Assembly**: Cached for 24 hours
- **Analysis Results**: Not cached (regenerated each request)

## Performance Summary

| Endpoint Type | Average Time | Description |
|---------------|--------------|-------------|
| Assembly | 5-10 seconds | Heavy processing (API calls, data processing) |
| Analysis | < 1 second | Light processing (chart generation) |
| Debug | < 1 second | Data inspection |

## Error Handling

All endpoints return appropriate HTTP status codes:

- `200` - Success
- `400` - Bad Request
- `404` - Not Found (league not found or expired)
- `500` - Internal Server Error

Error responses include error messages:
```json
{
  "error": "Description of the error"
}
```

## Usage Examples

### Python Example

```python
import requests

# 1. Assemble scoring data
assembly_response = requests.post(
    "http://127.0.0.1:8000/api/v1/leagues/assemble-scoring/",
    json={
        "platform": "espn",
        "league_id": "123456789",
        "s2": "your_s2_token",
        "swid": "your_swid_token"
    }
)

league_id = assembly_response.json()["league_id"]

# 2. Get analysis
analysis_response = requests.get(
    f"http://127.0.0.1:8000/api/v1/leagues/{league_id}/scoring/expected-wins/"
)

chart_html = analysis_response.json()["chart_html"]
```

### JavaScript Example

```javascript
// 1. Assemble scoring data
const assemblyResponse = await fetch('/api/v1/leagues/assemble-scoring/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        platform: 'espn',
        league_id: '123456789',
        s2: 'your_s2_token',
        swid: 'your_swid_token'
    })
});

const { league_id } = await assemblyResponse.json();

// 2. Get analysis
const analysisResponse = await fetch(`/api/v1/leagues/${league_id}/scoring/expected-wins/`);
const { chart_html } = await analysisResponse.json();

// 3. Render chart
document.getElementById('chart-container').innerHTML = chart_html;
```

## Testing

Run the comprehensive test script to verify all endpoints with timing data:

```bash
python3 test_api_comprehensive.py
```

This will test all endpoints and provide detailed timing information.

## Performance Notes

- Assembly endpoints are expensive (5-10 seconds) - call once and cache
- Analysis endpoints are fast (< 1 second) - call as needed
- Cache assembly results to avoid repeated processing
- Use separate assembly for scoring vs draft analysis
- Debug endpoint available for troubleshooting cached data 