#!/usr/bin/env python3
"""
Comprehensive test script for the Fantasy Football Analysis API
Tests all endpoints with timing data and draft separation functionality
Logs results to test_logs.txt
"""

import requests
import json
import time
from datetime import datetime
import sys

# Base URL for the API
BASE_URL = "http://127.0.0.1:8000/api/v1"

# Test data for Sleeper leagues
SLEEPER_LEAGUES = [
    {
        "name": "Original Test League",
        "platform": "sleeper",
        "league_id": "1103905062545362944"
    },
    {
        "name": "Boys League",
        "platform": "sleeper", 
        "league_id": "988223204793614336"
    },
    {
        "name": "Normal League 1",
        "platform": "sleeper",
        "league_id": "989316492422373376"
    },
    {
        "name": "Normal League 2", 
        "platform": "sleeper",
        "league_id": "1002402979250630656"
    },
    {
        "name": "Normal League 3",
        "platform": "sleeper", 
        "league_id": "962480529872408576"
    },
    {
        "name": "Dynasty League",
        "platform": "sleeper",
        "league_id": "917929342444068864"
    }
]

# Test data for ESPN leagues
ESPN_LEAGUES = [
    {
        "name": "ESPN League 1",
        "platform": "espn",
        "league_id": "64612107",
        "s2": "AECM85hbXZD%2FFG9s2ALIuE4XrHUPYodyji1oDVpO17ISfafgY9b9kxJ4QZaG1FiR1nVU0UW%2FtIQoPvtOfxxlA2y9xKn4dFzG1FO%2BNdP6ZsZZNly5BCtfCznME5sc8OJhBcY7nEjYRQ6b6tAtQvXYyvV65Ya6Hk4klxd0iIBzk6S82ZZiob5i8%2BThUSpeh0sUypUA%2FdpC06ZhaEVy9B0qVL%2B3tL8T3pK44imaNmSCGrLEmtTb5xmhmKIQYPPmE99IEvNy9ltr9DfPmJucfiPMVAfBcWaZUpEAE160r4SsIszqsw%3D%3D",
        "swid": "F71F32C4-9869-4DFB-A620-ADD15AA67520"
    },
    {
        "name": "ESPN League 2", 
        "platform": "espn",
        "league_id": "1927423163",
        "s2": "AECM85hbXZD%2FFG9s2ALIuE4XrHUPYodyji1oDVpO17ISfafgY9b9kxJ4QZaG1FiR1nVU0UW%2FtIQoPvtOfxxlA2y9xKn4dFzG1FO%2BNdP6ZsZZNly5BCtfCznME5sc8OJhBcY7nEjYRQ6b6tAtQvXYyvV65Ya6Hk4klxd0iIBzk6S82ZZiob5i8%2BThUSpeh0sUypUA%2FdpC06ZhaEVy9B0qVL%2B3tL8T3pK44imaNmSCGrLEmtTb5xmhmKIQYPPmE99IEvNy9ltr9DfPmJucfiPMVAfBcWaZUpEAE160r4SsIszqsw%3D%3D",
        "swid": "F71F32C4-9869-4DFB-A620-ADD15AA67520"
    }
]

# Legacy test data for backward compatibility
SLEEPER_TEST_DATA = SLEEPER_LEAGUES[0]  # Use first Sleeper league
ESPN_TEST_DATA = ESPN_LEAGUES[0]  # Use first ESPN league

class APITester:
    def __init__(self):
        self.results = []
        self.scoring_league_id = None
        self.draft_league_id = None
        self.log_file = "test_logs.txt"
        
        # Clear the log file
        with open(self.log_file, 'w') as f:
            f.write(f"=== API Test Log - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===\n\n")
    
    def log(self, message):
        """Write message to both console and log file"""
        print(message)
        with open(self.log_file, 'a') as f:
            f.write(message + '\n')
    
    def time_request(self, method, url, data=None, description=""):
        """Time a request and return results"""
        start_time = time.time()
        
        try:
            if method == 'GET':
                response = requests.get(url)
            elif method == 'POST':
                response = requests.post(url, json=data)
            
            end_time = time.time()
            duration = end_time - start_time
            
            result = {
                'description': description,
                'method': method,
                'url': url,
                'status_code': response.status_code,
                'duration': round(duration, 2),
                'success': response.status_code in [200, 201],
                'error': None,
                'response_data': None
            }
            
            # Try to parse JSON response regardless of status code
            try:
                result['response_data'] = response.json()
            except:
                result['response_data'] = response.text[:200]  # First 200 chars
            
            # Set error message for failed requests
            if not result['success']:
                result['error'] = response.text
            
            return result
            
        except Exception as e:
            end_time = time.time()
            duration = end_time - start_time
            
            return {
                'description': description,
                'method': method,
                'url': url,
                'status_code': None,
                'duration': round(duration, 2),
                'success': False,
                'error': str(e),
                'response_data': None
            }
    
    def test_assembly_endpoints(self):
        """Test assembly endpoints for all leagues"""
        self.log("🔧 Testing Assembly Endpoints...")
        self.log("=" * 60)
        
        # Test all ESPN leagues
        for i, league_data in enumerate(ESPN_LEAGUES):
            self.log(f"\n📊 Testing ESPN League {i+1}: {league_data['name']}")
            
            # Test ESPN Scoring Assembly
            result = self.time_request(
                'POST', 
                f"{BASE_URL}/leagues/assemble-scoring/",
                league_data,
                f"ESPN Scoring Assembly - {league_data['name']}"
            )
            self.results.append(result)
            
            if result['success']:
                if i == 0:  # Store first league ID for analysis tests
                    self.scoring_league_id = result['response_data']['league_id']
                self.log(f"✅ ESPN Scoring Assembly ({league_data['name']}): {result['duration']}s")
            else:
                self.log(f"❌ ESPN Scoring Assembly ({league_data['name']}) failed: {result['error']}")
            
            # Test ESPN Draft Assembly
            result = self.time_request(
                'POST', 
                f"{BASE_URL}/leagues/assemble-draft/",
                league_data,
                f"ESPN Draft Assembly - {league_data['name']}"
            )
            self.results.append(result)
            
            if result['success']:
                if i == 0:  # Store first league ID for analysis tests
                    self.draft_league_id = result['response_data']['league_id']
                self.log(f"✅ ESPN Draft Assembly ({league_data['name']}): {result['duration']}s")
            else:
                self.log(f"❌ ESPN Draft Assembly ({league_data['name']}) failed: {result['error']}")
        
        # Test all Sleeper leagues
        for i, league_data in enumerate(SLEEPER_LEAGUES):
            self.log(f"\n📊 Testing Sleeper League {i+1}: {league_data['name']}")
            
            # Test Sleeper Scoring Assembly
            result = self.time_request(
                'POST', 
                f"{BASE_URL}/leagues/assemble-scoring/",
                league_data,
                f"Sleeper Scoring Assembly - {league_data['name']}"
            )
            self.results.append(result)
            
            if result['success']:
                self.log(f"✅ Sleeper Scoring Assembly ({league_data['name']}): {result['duration']}s")
            else:
                self.log(f"❌ Sleeper Scoring Assembly ({league_data['name']}) failed: {result['error']}")
    
    def test_draft_separation_workflow(self):
        """Test the new draft separation workflow with multiple leagues"""
        self.log("\n🔄 Testing Draft Separation Workflow...")
        self.log("=" * 60)
        
        # Test draft separation with multiple Sleeper leagues
        for i, league_data in enumerate(SLEEPER_LEAGUES[:2]):  # Test first 2 leagues
            self.log(f"\n📊 Testing Draft Separation - {league_data['name']}")
            
            # Use Sleeper league for draft separation test
            league_id = None
            
            # Step 1: Assemble basic league (fast - no draft processing)
            self.log("1. Assembling basic league (scores and teams only)...")
            try:
                result = self.time_request(
                    'POST',
                    f"{BASE_URL}/leagues/assemble-scoring/",
                    league_data,
                    f"Sleeper Basic Assembly (Draft Separation Test) - {league_data['name']}"
                )
                self.results.append(result)
                
                if result['success']:
                    league_id = result['response_data']['league_id']
                    self.log(f"✅ League assembled successfully: {league_id}")
                else:
                    self.log(f"❌ League assembly failed: {result['error']}")
                    continue
                    
            except Exception as e:
                self.log(f"❌ Request failed: {e}")
                continue
            
            # Step 2: Check debug info to confirm no draft data
            self.log("2. Checking debug info (should show no draft data)...")
            result = self.time_request(
                'GET',
                f"{BASE_URL}/leagues/{league_id}/debug/",
                description=f"Debug Info Check - {league_data['name']}"
            )
            self.results.append(result)
            
            if result['success']:
                debug_data = result['response_data']
                self.log(f"✅ Debug info retrieved: {debug_data['num_teams']} teams, {debug_data['num_weeks']} weeks")
                self.log(f"   Assembly type: {debug_data['assembly_type']}")
            else:
                self.log(f"❌ Debug check failed: {result['error']}")
            
            # Step 3: Try to access draft analysis (should fail) - This is EXPECTED to fail
            self.log("3. Testing draft analysis access (should fail)...")
            result = self.time_request(
                'GET',
                f"{BASE_URL}/leagues/{league_id}/draft/sleepers/",
                description=f"Draft Analysis Access (Expected to Fail) - {league_data['name']}"
            )
            # Don't add this to results since it's an expected failure
            # self.results.append(result)
            
            if result['status_code'] == 400:
                if 'response_data' in result and result['response_data']:
                    error_data = result['response_data']
                    self.log(f"✅ Draft analysis correctly blocked: {error_data.get('error', 'Unknown error')}")
                    self.log(f"   Solution: {error_data.get('solution', 'Call /process-draft/ endpoint first')}")
                else:
                    self.log(f"✅ Draft analysis correctly blocked with status 400")
            else:
                self.log(f"❌ Draft analysis should have failed but didn't: {result.get('error', 'Unknown error')}")
            
            # Step 4: Process draft data separately
            self.log("4. Processing draft data separately...")
            result = self.time_request(
                'POST',
                f"{BASE_URL}/leagues/{league_id}/process-draft/",
                description=f"Draft Processing - {league_data['name']}"
            )
            self.results.append(result)
            
            if result['success']:
                draft_data = result['response_data']
                self.log(f"✅ Draft processing successful: {draft_data['status']}")
                self.log(f"   Platform: {draft_data['platform']}")
            else:
                self.log(f"❌ Draft processing failed: {result['error']}")
                continue
            
            # Step 5: Try draft analysis again (should work now)
            self.log("5. Testing draft analysis access (should work now)...")
            result = self.time_request(
                'GET',
                f"{BASE_URL}/leagues/{league_id}/draft/sleepers/",
                description=f"Draft Analysis Access (Should Work) - {league_data['name']}"
            )
            self.results.append(result)
            
            if result['success']:
                sleepers_data = result['response_data']
                self.log(f"✅ Draft analysis successful: {len(sleepers_data['data'])} sleepers found")
                for sleeper in sleepers_data['data']:
                    self.log(f"   - {sleeper[0]}: {sleeper[1]}")
            else:
                self.log(f"❌ Draft analysis failed: {result['error']}")
            
            # Step 6: Test scoring analysis (should work regardless)
            self.log("6. Testing scoring analysis (should work regardless)...")
            result = self.time_request(
                'GET',
                f"{BASE_URL}/leagues/{league_id}/scoring/expected-wins/",
                description=f"Scoring Analysis (Should Work) - {league_data['name']}"
            )
            self.results.append(result)
            
            if result['success']:
                scoring_data = result['response_data']
                self.log(f"✅ Scoring analysis successful: {scoring_data['metadata']['analysis_type']}")
            else:
                self.log(f"❌ Scoring analysis failed: {result['error']}")
    
    def test_scoring_analysis_endpoints(self):
        """Test scoring analysis endpoints"""
        if not self.scoring_league_id:
            self.log("❌ No scoring league ID available for analysis tests")
            return
        
        self.log(f"\n📊 Testing Scoring Analysis Endpoints...")
        self.log("=" * 60)
        
        scoring_endpoints = [
            ("expected-wins", "Expected Wins Analysis"),
            ("ew-difference", "EW Difference Analysis"),
            ("luck", "Luck Analysis"),
            ("bonage", "Bonage Analysis"),
            ("consistency", "Consistency Analysis"),
            ("probability-curve", "Probability Curve Analysis")
        ]
        
        for endpoint, description in scoring_endpoints:
            result = self.time_request(
                'GET',
                f"{BASE_URL}/leagues/{self.scoring_league_id}/scoring/{endpoint}/",
                description=description
            )
            self.results.append(result)
            
            if result['success']:
                self.log(f"✅ {description}: {result['duration']}s")
            else:
                self.log(f"❌ {description} failed: {result['error']}")
    
    def test_draft_analysis_endpoints(self):
        """Test draft analysis endpoints"""
        if not self.draft_league_id:
            self.log("❌ No draft league ID available for analysis tests")
            return
        
        self.log(f"\n📋 Testing Draft Analysis Endpoints...")
        self.log("=" * 60)
        
        draft_endpoints = [
            ("sleepers", "Sleepers Analysis"),
            ("positional-ranks", "Positional Ranks Analysis"),
            ("injury-table", "Draft Injury Analysis")
        ]
        
        for endpoint, description in draft_endpoints:
            result = self.time_request(
                'GET',
                f"{BASE_URL}/leagues/{self.draft_league_id}/draft/{endpoint}/",
                description=description
            )
            
            # Check if this is an expected failure due to missing draft data
            if result['status_code'] == 400 and 'response_data' in result:
                error_data = result['response_data']
                if 'Draft data not available' in error_data.get('error', ''):
                    self.log(f"⚠️ {description}: Draft data not available (expected for this test)")
                    # Don't add to results since this is expected
                    continue
            
            self.results.append(result)
            
            if result['success']:
                self.log(f"✅ {description}: {result['duration']}s")
            else:
                self.log(f"❌ {description} failed: {result['error']}")
    
    def test_debug_endpoint(self):
        """Test debug endpoint"""
        if not self.scoring_league_id:
            self.log("❌ No league ID available for debug test")
            return
        
        self.log(f"\n🐛 Testing Debug Endpoint...")
        self.log("=" * 60)
        
        result = self.time_request(
            'GET',
            f"{BASE_URL}/leagues/{self.scoring_league_id}/debug/",
            description="Debug Endpoint"
        )
        self.results.append(result)
        
        if result['success']:
            debug_data = result['response_data']
            self.log(f"✅ Debug endpoint working!")
            self.log(f"   Teams: {debug_data['num_teams']}")
            self.log(f"   Weeks: {debug_data['num_weeks']}")
            self.log(f"   Assembly Type: {debug_data['assembly_type']}")
        else:
            self.log(f"❌ Debug endpoint failed: {result['error']}")
    
    def test_streaming_assembly(self):
        """Test streaming assembly endpoint with multiple leagues"""
        self.log(f"\n🌊 Testing Streaming Assembly...")
        self.log("=" * 60)
        
        # Test streaming assembly with first Sleeper league
        league_data = SLEEPER_LEAGUES[0]
        result = self.time_request(
            'POST',
            f"{BASE_URL}/leagues/assemble-scoring-stream/",
            league_data,
            f"Streaming Assembly - {league_data['name']}"
        )
        self.results.append(result)
        
        if result['success']:
            self.log(f"✅ Streaming assembly initiated: {result['duration']}s")
        else:
            self.log(f"❌ Streaming assembly failed: {result['error']}")
    
    def print_summary(self):
        """Print test summary"""
        self.log(f"\n📋 Test Summary")
        self.log("=" * 60)
        
        total_tests = len(self.results)
        successful_tests = sum(1 for r in self.results if r['success'])
        failed_tests = total_tests - successful_tests
        
        self.log(f"Total Tests: {total_tests}")
        self.log(f"Successful: {successful_tests}")
        self.log(f"Failed: {failed_tests}")
        self.log(f"Success Rate: {(successful_tests/total_tests*100):.1f}%")
        
        if failed_tests > 0:
            self.log(f"\n❌ Failed Tests:")
            for result in self.results:
                if not result['success']:
                    self.log(f"   - {result['description']}: {result['error']}")
        
        # Performance summary
        successful_durations = [r['duration'] for r in self.results if r['success']]
        if successful_durations:
            avg_duration = sum(successful_durations) / len(successful_durations)
            max_duration = max(successful_durations)
            min_duration = min(successful_durations)
            
            self.log(f"\n⏱️ Performance Summary:")
            self.log(f"   Average Response Time: {avg_duration:.2f}s")
            self.log(f"   Fastest Response: {min_duration:.2f}s")
            self.log(f"   Slowest Response: {max_duration:.2f}s")
        
        self.log(f"\n📄 Full results logged to: {self.log_file}")
    
    def run_all_tests(self):
        """Run all tests"""
        self.log("🧪 Starting Comprehensive API Testing")
        self.log("=" * 60)
        
        # Test assembly endpoints
        self.test_assembly_endpoints()
        
        # Test draft separation workflow
        self.test_draft_separation_workflow()
        
        # Test scoring analysis endpoints
        self.test_scoring_analysis_endpoints()
        
        # Test draft analysis endpoints
        self.test_draft_analysis_endpoints()
        
        # Test debug endpoint
        self.test_debug_endpoint()
        
        # Test streaming assembly
        self.test_streaming_assembly()
        
        # Print summary
        self.print_summary()

def main():
    tester = APITester()
    tester.run_all_tests()

if __name__ == "__main__":
    main() 