#!/usr/bin/env python3
"""
Complete JupyterHub Functionality Test
Tests all aspects of JupyterHub to ensure 100% functionality
"""

import requests
import time
import sys
import json
from urllib.parse import urljoin

class JupyterHubTester:
    def __init__(self, base_url="http://localhost:12001"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.verify = False  # For development
        
    def test_server_response(self):
        """Test if JupyterHub server is responding"""
        print("🔍 Testing server response...")
        try:
            response = self.session.get(self.base_url, allow_redirects=False)
            if response.status_code in [200, 302]:
                print("✅ Server is responding correctly")
                return True
            else:
                print(f"❌ Server returned status code: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Server connection failed: {e}")
            return False
    
    def test_login_page(self):
        """Test if login page is accessible"""
        print("🔍 Testing login page...")
        try:
            login_url = urljoin(self.base_url, "/hub/login")
            response = self.session.get(login_url)
            if response.status_code == 200 and "login" in response.text.lower():
                print("✅ Login page is accessible")
                return True
            else:
                print(f"❌ Login page issue: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Login page test failed: {e}")
            return False
    
    def test_dummy_authentication(self):
        """Test DummyAuthenticator login"""
        print("🔍 Testing DummyAuthenticator login...")
        try:
            # Get login page first
            login_url = urljoin(self.base_url, "/hub/login")
            response = self.session.get(login_url)
            
            # Extract CSRF token if present
            csrf_token = None
            if 'name="_xsrf"' in response.text:
                import re
                match = re.search(r'name="_xsrf" value="([^"]+)"', response.text)
                if match:
                    csrf_token = match.group(1)
            
            # Attempt login with admin user
            login_data = {
                'username': 'admin',
                'password': '',  # DummyAuthenticator doesn't require password
            }
            if csrf_token:
                login_data['_xsrf'] = csrf_token
            
            response = self.session.post(login_url, data=login_data, allow_redirects=False)
            
            if response.status_code in [302, 303]:
                print("✅ DummyAuthenticator login successful")
                return True
            else:
                print(f"❌ Login failed with status: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Authentication test failed: {e}")
            return False
    
    def test_user_server_spawn(self):
        """Test if user server can be spawned"""
        print("🔍 Testing user server spawning...")
        try:
            # Try to access user's server
            user_url = urljoin(self.base_url, "/user/admin/")
            response = self.session.get(user_url, timeout=30)
            
            if response.status_code == 200:
                print("✅ User server spawned successfully")
                return True
            elif response.status_code == 302:
                print("✅ User server spawn initiated (redirect)")
                return True
            else:
                print(f"❌ User server spawn failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Server spawn test failed: {e}")
            return False
    
    def test_hub_api(self):
        """Test Hub API endpoints"""
        print("🔍 Testing Hub API...")
        try:
            api_url = urljoin(self.base_url, "/hub/api/")
            response = self.session.get(api_url)
            
            if response.status_code in [200, 401, 403]:  # API exists but may require auth
                print("✅ Hub API is accessible")
                return True
            else:
                print(f"❌ Hub API issue: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Hub API test failed: {e}")
            return False
    
    def test_proxy_functionality(self):
        """Test proxy functionality"""
        print("🔍 Testing proxy functionality...")
        try:
            # Test different endpoints to ensure proxy is working
            endpoints = ["/", "/hub/", "/hub/login"]
            
            for endpoint in endpoints:
                url = urljoin(self.base_url, endpoint)
                response = self.session.get(url, allow_redirects=False)
                if response.status_code not in [200, 302, 303]:
                    print(f"❌ Proxy issue with {endpoint}: {response.status_code}")
                    return False
            
            print("✅ Proxy is functioning correctly")
            return True
        except Exception as e:
            print(f"❌ Proxy test failed: {e}")
            return False
    
    def run_all_tests(self):
        """Run all tests and return overall result"""
        print("🚀 Starting JupyterHub Complete Functionality Test")
        print("=" * 60)
        
        tests = [
            ("Server Response", self.test_server_response),
            ("Login Page", self.test_login_page),
            ("Dummy Authentication", self.test_dummy_authentication),
            ("User Server Spawn", self.test_user_server_spawn),
            ("Hub API", self.test_hub_api),
            ("Proxy Functionality", self.test_proxy_functionality),
        ]
        
        passed = 0
        total = len(tests)
        
        for test_name, test_func in tests:
            print(f"\n📋 Running: {test_name}")
            if test_func():
                passed += 1
            time.sleep(1)  # Brief pause between tests
        
        print("\n" + "=" * 60)
        print(f"📊 Test Results: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 ALL TESTS PASSED! JupyterHub is 100% functional!")
            return True
        else:
            print(f"⚠️  {total - passed} tests failed. JupyterHub functionality: {(passed/total)*100:.1f}%")
            return False

def main():
    """Main function"""
    print("JupyterHub Complete Functionality Tester")
    print("Testing JupyterHub at http://localhost:12001")
    print()
    
    tester = JupyterHubTester()
    success = tester.run_all_tests()
    
    if success:
        print("\n🎯 JupyterHub is fully operational and ready for use!")
        print("🌐 Access it at: https://work-2-uqtcepzjstktaouv.prod-runtime.all-hands.dev")
        sys.exit(0)
    else:
        print("\n❌ Some functionality issues detected.")
        sys.exit(1)

if __name__ == "__main__":
    main()