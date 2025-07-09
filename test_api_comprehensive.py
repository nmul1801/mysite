#!/usr/bin/env python3
"""
Comprehensive test script for the Fantasy Football Analysis API
Tests all endpoints with timing data
"""

import requests
import json
import time
from datetime import datetime

# Base URL for the API
BASE_URL = "http://127.0.0.1:8000/api/v1"

# Test data for Sleeper league (from the code)
SLEEPER_TEST_DATA = {
    "platform": "sleeper",
    "league_id": "1103905062545362944"  # Updated with correct Sleeper league ID
}

# Test data for ESPN league (from the code)
ESPN_TEST_DATA = {
    "platform": "espn",
    "league_id": "1927423163",
    "s2": "AECM85hbXZD%2FFG9s2ALIuE4XrHUPYodyji1oDVpO17ISfafgY9b9kxJ4QZaG1FiR1nVU0UW%2FtIQoPvtOfxxlA2y9xKn4dFzG1FO%2BNdP6ZsZZNly5BCtfCznME5sc8OJhBcY7nEjYRQ6b6tAtQvXYyvV65Ya6Hk4klxd0iIBzk6S82ZZiob5i8%2BThUSpeh0sUypUA%2FdpC06ZhaEVy9B0qVL%2B3tL8T3pK44imaNmSCGrLEmtTb5xmhmKIQYPPmE99IEvNy9ltr9DfPmJucfiPMVAfBcWaZUpEAE160r4SsIszqsw%3D%3D",
    "swid": "F71F32C4-9869-4DFB-A620-ADD15AA67520"
}

class APITester:
    def __init__(self):
        self.results = []
        self.scoring_league_id = None
        self.draft_league_id = None
    
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
                'error': None
            }
            
            if response.status_code in [200, 201]:
                try:
                    result['response_data'] = response.json()
                except:
                    result['response_data'] = response.text[:200]  # First 200 chars
            else:
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
        """Test assembly endpoints"""
        print("🔧 Testing Assembly Endpoints...")
        print("=" * 60)
        
        # Test ESPN Scoring Assembly
        result = self.time_request(
            'POST', 
            f"{BASE_URL}/leagues/assemble-scoring/",
            ESPN_TEST_DATA,
            "ESPN Scoring Assembly"
        )
        self.results.append(result)
        
        if result['success']:
            self.scoring_league_id = result['response_data']['league_id']
            print(f"✅ ESPN Scoring Assembly: {result['duration']}s")
        else:
            print(f"❌ ESPN Scoring Assembly failed: {result['error']}")
        
        # Test ESPN Draft Assembly
        result = self.time_request(
            'POST', 
            f"{BASE_URL}/leagues/assemble-draft/",
            ESPN_TEST_DATA,
            "ESPN Draft Assembly"
        )
        self.results.append(result)
        
        if result['success']:
            self.draft_league_id = result['response_data']['league_id']
            print(f"✅ ESPN Draft Assembly: {result['duration']}s")
        else:
            print(f"❌ ESPN Draft Assembly failed: {result['error']}")
        
        # Test Sleeper Scoring Assembly
        result = self.time_request(
            'POST', 
            f"{BASE_URL}/leagues/assemble-scoring/",
            SLEEPER_TEST_DATA,
            "Sleeper Scoring Assembly"
        )
        self.results.append(result)
        
        if result['success']:
            print(f"✅ Sleeper Scoring Assembly: {result['duration']}s")
        else:
            print(f"❌ Sleeper Scoring Assembly failed: {result['error']}")
    
    def test_scoring_analysis_endpoints(self):
        """Test scoring analysis endpoints"""
        if not self.scoring_league_id:
            print("❌ No scoring league ID available for analysis tests")
            return
        
        print(f"\n📊 Testing Scoring Analysis Endpoints...")
        print("=" * 60)
        
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
                print(f"✅ {description}: {result['duration']}s")
            else:
                print(f"❌ {description} failed: {result['error']}")
    
    def test_draft_analysis_endpoints(self):
        """Test draft analysis endpoints"""
        if not self.draft_league_id:
            print("❌ No draft league ID available for analysis tests")
            return
        
        print(f"\n📋 Testing Draft Analysis Endpoints...")
        print("=" * 60)
        
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
            self.results.append(result)
            
            if result['success']:
                print(f"✅ {description}: {result['duration']}s")
            else:
                print(f"❌ {description} failed: {result['error']}")
    
    def test_debug_endpoint(self):
        """Test debug endpoint"""
        if not self.scoring_league_id:
            print("❌ No league ID available for debug test")
            return
        
        print(f"\n🐛 Testing Debug Endpoint...")
        print("=" * 60)
        
        result = self.time_request(
            'GET',
            f"{BASE_URL}/leagues/{self.scoring_league_id}/debug/",
            description="Debug League Info"
        )
        self.results.append(result)
        
        if result['success']:
            print(f"✅ Debug Endpoint: {result['duration']}s")
        else:
            print(f"❌ Debug Endpoint failed: {result['error']}")
    
    def print_summary(self):
        """Print comprehensive test summary"""
        print(f"\n📈 TEST SUMMARY")
        print("=" * 60)
        
        successful_tests = [r for r in self.results if r['success']]
        failed_tests = [r for r in self.results if not r['success']]
        
        print(f"Total Tests: {len(self.results)}")
        print(f"Successful: {len(successful_tests)}")
        print(f"Failed: {len(failed_tests)}")
        print(f"Success Rate: {(len(successful_tests)/len(self.results)*100):.1f}%")
        
        if successful_tests:
            assembly_tests = [r for r in successful_tests if 'Assembly' in r['description']]
            analysis_tests = [r for r in successful_tests if 'Analysis' in r['description']]
            
            if assembly_tests:
                avg_assembly_time = sum(r['duration'] for r in assembly_tests) / len(assembly_tests)
                print(f"\n🏗️  Assembly Endpoints (avg): {avg_assembly_time:.2f}s")
            
            if analysis_tests:
                avg_analysis_time = sum(r['duration'] for r in analysis_tests) / len(analysis_tests)
                print(f"📊 Analysis Endpoints (avg): {avg_analysis_time:.2f}s")
        
        print(f"\n⏱️  Detailed Timing:")
        print("-" * 40)
        for result in self.results:
            status = "✅" if result['success'] else "❌"
            print(f"{status} {result['description']}: {result['duration']}s")
        
        if failed_tests:
            print(f"\n❌ Failed Tests:")
            print("-" * 40)
            for result in failed_tests:
                print(f"• {result['description']}: {result['error']}")
    
    def run_all_tests(self):
        """Run all tests"""
        print("🧪 COMPREHENSIVE API TESTING")
        print("=" * 60)
        print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        
        # Run all test suites
        self.test_assembly_endpoints()
        self.test_scoring_analysis_endpoints()
        self.test_draft_analysis_endpoints()
        self.test_debug_endpoint()
        
        # Print summary
        self.print_summary()
        
        print(f"\n🏁 Testing completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

def main():
    tester = APITester()
    tester.run_all_tests()

if __name__ == "__main__":
    main() 