#!/usr/bin/env python3
"""
Test script for the Fantasy Football Analysis API
"""

import requests
import json

# Base URL for the API
BASE_URL = "http://127.0.0.1:8000/api/v1"

def test_assembly_endpoint():
    """Test the league assembly endpoint"""
    print("Testing league assembly endpoint...")
    
    # Test data for ESPN league
    test_data = {
        "platform": "espn",
        "league_id": "1927423163",  # Use your actual league ID
        "s2": "AECM85hbXZD%2FFG9s2ALIuE4XrHUPYodyji1oDVpO17ISfafgY9b9kxJ4QZaG1FiR1nVU0UW%2FtIQoPvtOfxxlA2y9xKn4dFzG1FO%2BNdP6ZsZZNly5BCtfCznME5sc8OJhBcY7nEjYRQ6b6tAtQvXYyvV65Ya6Hk4klxd0iIBzk6S82ZZiob5i8%2BThUSpeh0sUypUA%2FdpC06ZhaEVy9B0qVL%2B3tL8T3pK44imaNmSCGrLEmtTb5xmhmKIQYPPmE99IEvNy9ltr9DfPmJucfiPMVAfBcWaZUpEAE160r4SsIszqsw%3D%3D",
        "swid": "F71F32C4-9869-4DFB-A620-ADD15AA67520"
    }
    
    try:
        # Test scoring assembly
        response = requests.post(f"{BASE_URL}/leagues/assemble-scoring/", json=test_data)
        print(f"Scoring Assembly Status: {response.status_code}")
        
        if response.status_code == 201:
            data = response.json()
            print(f"League ID: {data.get('league_id')}")
            print(f"Teams: {data.get('teams')}")
            print(f"Num Teams: {data.get('num_teams')}")
            print(f"Num Weeks: {data.get('num_weeks')}")
            return data.get('league_id')
        else:
            print(f"Error: {response.text}")
            return None
            
    except Exception as e:
        print(f"Exception: {e}")
        return None

def test_analysis_endpoint(league_id):
    """Test an analysis endpoint"""
    if not league_id:
        print("No league ID available for testing")
        return
    
    print(f"\nTesting analysis endpoint with league_id: {league_id}")
    
    try:
        # Test expected wins analysis
        response = requests.get(f"{BASE_URL}/leagues/{league_id}/scoring/expected-wins/")
        print(f"Expected Wins Analysis Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Analysis Type: {data.get('metadata', {}).get('analysis_type')}")
            print(f"Chart Type: {data.get('metadata', {}).get('chart_type')}")
            print(f"Chart HTML Length: {len(data.get('chart_html', ''))}")
            print("✅ Analysis endpoint working!")
        else:
            print(f"Error: {response.text}")
            
    except Exception as e:
        print(f"Exception: {e}")

def main():
    print("🧪 Testing Fantasy Football Analysis API")
    print("=" * 50)
    
    # Test assembly
    league_id = test_assembly_endpoint()
    
    # Test analysis
    test_analysis_endpoint(league_id)
    
    print("\n" + "=" * 50)
    print("✅ API testing complete!")

if __name__ == "__main__":
    main() 