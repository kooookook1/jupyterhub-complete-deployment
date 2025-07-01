#!/usr/bin/env python3
"""
Test spawning functionality with detailed debugging
"""

import requests
import time
import sys
from urllib.parse import urljoin
from bs4 import BeautifulSoup

class SpawnTester:
    def __init__(self, base_url="http://localhost:12001"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.verify = False
        
    def get_xsrf_token(self, html_content):
        """Extract XSRF token from HTML"""
        soup = BeautifulSoup(html_content, 'html.parser')
        xsrf_input = soup.find('input', {'name': '_xsrf'})
        if xsrf_input:
            return xsrf_input.get('value')
        return None
    
    def test_login_and_spawn(self):
        """Test login and spawning process"""
        print("🔍 Testing login and spawn process...")
        
        # Step 1: Get login page
        print("  📋 Getting login page...")
        login_url = urljoin(self.base_url, '/hub/login')
        response = self.session.get(login_url)
        
        if response.status_code != 200:
            print(f"  ❌ Failed to get login page: {response.status_code}")
            return False
            
        # Step 2: Extract XSRF token
        xsrf_token = self.get_xsrf_token(response.text)
        if not xsrf_token:
            print("  ❌ Could not extract XSRF token")
            return False
        print(f"  ✅ Got XSRF token: {xsrf_token[:20]}...")
        
        # Step 3: Login
        print("  📋 Logging in...")
        login_data = {
            'username': 'admin',
            'password': '',
            '_xsrf': xsrf_token
        }
        
        response = self.session.post(login_url, data=login_data, allow_redirects=False)
        print(f"  📊 Login response: {response.status_code}")
        
        if response.status_code == 302:
            print("  ✅ Login successful (redirected)")
            redirect_url = response.headers.get('Location', '')
            print(f"  📍 Redirected to: {redirect_url}")
        else:
            print(f"  ❌ Login failed: {response.status_code}")
            print(f"  📄 Response: {response.text[:200]}...")
            return False
        
        # Step 4: Follow redirect to spawn
        if redirect_url.startswith('/'):
            spawn_url = urljoin(self.base_url, redirect_url)
        else:
            spawn_url = redirect_url
            
        print(f"  📋 Following redirect to: {spawn_url}")
        response = self.session.get(spawn_url, allow_redirects=False)
        print(f"  📊 Spawn page response: {response.status_code}")
        
        if response.status_code == 200:
            print("  ✅ Spawn page loaded successfully")
            # Check if it's a spawn form or already spawned
            if 'spawn' in response.text.lower():
                print("  📋 Found spawn form, attempting to spawn...")
                return self.attempt_spawn(response.text, spawn_url)
            else:
                print("  ℹ️  No spawn form found, checking content...")
                print(f"  📄 Content preview: {response.text[:200]}...")
        elif response.status_code == 302:
            print("  📍 Another redirect...")
            next_url = response.headers.get('Location', '')
            print(f"  📍 Next URL: {next_url}")
            
            # Follow the next redirect
            if next_url.startswith('/'):
                next_url = urljoin(self.base_url, next_url)
            response = self.session.get(next_url)
            print(f"  📊 Final response: {response.status_code}")
            
            if response.status_code == 424:
                print("  ❌ Got 424 Failed Dependency - spawning failed")
                return False
            elif response.status_code == 200:
                print("  ✅ Got 200 - checking if it's a notebook server...")
                if 'jupyter' in response.text.lower() or 'notebook' in response.text.lower():
                    print("  🎯 Successfully spawned notebook server!")
                    return True
                else:
                    print("  ⚠️  Got 200 but doesn't look like a notebook server")
                    print(f"  📄 Content preview: {response.text[:200]}...")
        
        return False
    
    def attempt_spawn(self, html_content, spawn_url):
        """Attempt to spawn server using form"""
        print("  📋 Attempting to spawn server...")
        
        # Extract XSRF token from spawn form
        xsrf_token = self.get_xsrf_token(html_content)
        if not xsrf_token:
            print("  ❌ Could not extract XSRF token from spawn form")
            return False
        
        # Submit spawn form
        spawn_data = {
            '_xsrf': xsrf_token
        }
        
        response = self.session.post(spawn_url, data=spawn_data, allow_redirects=False)
        print(f"  📊 Spawn submit response: {response.status_code}")
        
        if response.status_code == 302:
            print("  ✅ Spawn submitted successfully (redirected)")
            redirect_url = response.headers.get('Location', '')
            print(f"  📍 Redirected to: {redirect_url}")
            
            # Follow redirect to user server
            if redirect_url.startswith('/'):
                user_url = urljoin(self.base_url, redirect_url)
            else:
                user_url = redirect_url
                
            print(f"  📋 Checking user server at: {user_url}")
            
            # Wait a bit for server to start
            for i in range(10):
                print(f"  ⏳ Waiting for server to start... ({i+1}/10)")
                time.sleep(2)
                
                response = self.session.get(user_url)
                print(f"  📊 User server response: {response.status_code}")
                
                if response.status_code == 200:
                    print("  🎯 User server is running!")
                    return True
                elif response.status_code == 424:
                    print("  ⚠️  Still getting 424, server not ready yet...")
                    continue
                else:
                    print(f"  ❓ Unexpected response: {response.status_code}")
            
            print("  ❌ Server failed to start within timeout")
            return False
        else:
            print(f"  ❌ Spawn submit failed: {response.status_code}")
            return False

def main():
    """Main function"""
    print("🚀 JupyterHub Spawn Debug Tester")
    print("=" * 50)
    
    tester = SpawnTester()
    success = tester.test_login_and_spawn()
    
    if success:
        print("\n🎯 Spawning test successful!")
        sys.exit(0)
    else:
        print("\n❌ Spawning test failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()