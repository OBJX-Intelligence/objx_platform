#!/usr/bin/env python3
"""
OBJX Platform - Advanced MEM0 API Test Script
Tests different authentication methods and API endpoints for MEM0
"""

import os
import sys
import json
import time
import requests
import base64

# ANSI color codes for terminal output
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_header(text):
    """Print a formatted header"""
    print(f"\n{Colors.BLUE}{Colors.BOLD}{'=' * 60}{Colors.END}")
    print(f"{Colors.BLUE}{Colors.BOLD}{text.center(60)}{Colors.END}")
    print(f"{Colors.BLUE}{Colors.BOLD}{'=' * 60}{Colors.END}\n")

def print_success(text):
    """Print a success message"""
    print(f"{Colors.GREEN}✓ {text}{Colors.END}")

def print_warning(text):
    """Print a warning message"""
    print(f"{Colors.YELLOW}⚠ {text}{Colors.END}")

def print_error(text):
    """Print an error message"""
    print(f"{Colors.RED}✗ {text}{Colors.END}")

def print_info(text):
    """Print an info message"""
    print(f"{Colors.BLUE}ℹ {text}{Colors.END}")

def test_mem0_auth_method1(api_key):
    """Test MEM0 API with Bearer token authentication"""
    print_header("TESTING MEM0 API - BEARER TOKEN AUTH")
    
    print_info(f"API Key: {api_key[:5]}...{api_key[-4:]}")
    
    try:
        # Create a test memory
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        
        # Test creating a memory
        create_url = "https://api.mem0.ai/v1/memories"
        create_payload = {
            "content": "This is a test memory from OBJX Platform using Bearer token",
            "metadata": {
                "source": "OBJX Platform Test",
                "timestamp": time.time()
            }
        }
        
        print_info("Attempting to create a test memory...")
        create_response = requests.post(create_url, headers=headers, json=create_payload)
        
        print_info(f"Status code: {create_response.status_code}")
        print_info(f"Response: {create_response.text}")
        
        if create_response.status_code == 200 or create_response.status_code == 201:
            print_success("Bearer token authentication successful")
            return True
        else:
            print_error("Bearer token authentication failed")
            return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False

def test_mem0_auth_method2(api_key):
    """Test MEM0 API with API key in header"""
    print_header("TESTING MEM0 API - API KEY IN HEADER")
    
    print_info(f"API Key: {api_key[:5]}...{api_key[-4:]}")
    
    try:
        # Create a test memory
        headers = {
            "Content-Type": "application/json",
            "X-API-Key": api_key
        }
        
        # Test creating a memory
        create_url = "https://api.mem0.ai/v1/memories"
        create_payload = {
            "content": "This is a test memory from OBJX Platform using X-API-Key",
            "metadata": {
                "source": "OBJX Platform Test",
                "timestamp": time.time()
            }
        }
        
        print_info("Attempting to create a test memory...")
        create_response = requests.post(create_url, headers=headers, json=create_payload)
        
        print_info(f"Status code: {create_response.status_code}")
        print_info(f"Response: {create_response.text}")
        
        if create_response.status_code == 200 or create_response.status_code == 201:
            print_success("X-API-Key authentication successful")
            return True
        else:
            print_error("X-API-Key authentication failed")
            return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False

def test_mem0_auth_method3(api_key):
    """Test MEM0 API with Basic authentication"""
    print_header("TESTING MEM0 API - BASIC AUTH")
    
    print_info(f"API Key: {api_key[:5]}...{api_key[-4:]}")
    
    try:
        # Create basic auth header
        auth_header = base64.b64encode(f"{api_key}:".encode()).decode()
        
        # Create a test memory
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Basic {auth_header}"
        }
        
        # Test creating a memory
        create_url = "https://api.mem0.ai/v1/memories"
        create_payload = {
            "content": "This is a test memory from OBJX Platform using Basic auth",
            "metadata": {
                "source": "OBJX Platform Test",
                "timestamp": time.time()
            }
        }
        
        print_info("Attempting to create a test memory...")
        create_response = requests.post(create_url, headers=headers, json=create_payload)
        
        print_info(f"Status code: {create_response.status_code}")
        print_info(f"Response: {create_response.text}")
        
        if create_response.status_code == 200 or create_response.status_code == 201:
            print_success("Basic authentication successful")
            return True
        else:
            print_error("Basic authentication failed")
            return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False

def test_mem0_auth_method4(api_key):
    """Test MEM0 API with query parameter"""
    print_header("TESTING MEM0 API - QUERY PARAMETER")
    
    print_info(f"API Key: {api_key[:5]}...{api_key[-4:]}")
    
    try:
        # Create a test memory
        headers = {
            "Content-Type": "application/json"
        }
        
        # Test creating a memory
        create_url = f"https://api.mem0.ai/v1/memories?api_key={api_key}"
        create_payload = {
            "content": "This is a test memory from OBJX Platform using query parameter",
            "metadata": {
                "source": "OBJX Platform Test",
                "timestamp": time.time()
            }
        }
        
        print_info("Attempting to create a test memory...")
        create_response = requests.post(create_url, headers=headers, json=create_payload)
        
        print_info(f"Status code: {create_response.status_code}")
        print_info(f"Response: {create_response.text}")
        
        if create_response.status_code == 200 or create_response.status_code == 201:
            print_success("Query parameter authentication successful")
            return True
        else:
            print_error("Query parameter authentication failed")
            return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False

def test_mem0_alternative_endpoints(api_key):
    """Test alternative MEM0 API endpoints"""
    print_header("TESTING MEM0 API - ALTERNATIVE ENDPOINTS")
    
    print_info(f"API Key: {api_key[:5]}...{api_key[-4:]}")
    
    # List of potential endpoints to try
    endpoints = [
        "https://api.mem0.ai/v1/memories",
        "https://api.mem0.ai/v1/memory",
        "https://api.mem0.ai/memories",
        "https://mem0.ai/api/v1/memories",
        "https://mem0.ai/api/memories"
    ]
    
    for endpoint in endpoints:
        print_info(f"Testing endpoint: {endpoint}")
        
        try:
            # Try different auth methods
            headers_options = [
                {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"},
                {"Content-Type": "application/json", "X-API-Key": api_key},
                {"Content-Type": "application/json"}
            ]
            
            for headers in headers_options:
                auth_type = "Bearer" if "Bearer" in str(headers) else "X-API-Key" if "X-API-Key" in str(headers) else "None"
                print_info(f"Trying auth type: {auth_type}")
                
                create_payload = {
                    "content": f"This is a test memory from OBJX Platform using endpoint {endpoint}",
                    "metadata": {
                        "source": "OBJX Platform Test",
                        "timestamp": time.time()
                    }
                }
                
                # Add query param if no auth in headers
                url = endpoint
                if auth_type == "None":
                    url = f"{endpoint}?api_key={api_key}"
                
                create_response = requests.post(url, headers=headers, json=create_payload)
                
                print_info(f"Status code: {create_response.status_code}")
                
                if create_response.status_code == 200 or create_response.status_code == 201:
                    print_success(f"Success with endpoint {endpoint} and auth {auth_type}")
                    return True, endpoint, headers
        except Exception as e:
            print_warning(f"Error with endpoint {endpoint}: {str(e)}")
    
    print_error("All alternative endpoints failed")
    return False, None, None

def main():
    """Main function to test MEM0 API"""
    print_header("OBJX PLATFORM - ADVANCED MEM0 API TESTS")
    
    # Test keys
    keys = [
        "m0-NYHyffT0aUwQUxxP8yleXWMcob6y1WkeBscMb2UH",
        "m0-iL5CB1HAi2fONORs9JialJXrS1xZfXS0HATj3W7i"
    ]
    
    # Try both keys with different auth methods
    for key in keys:
        print_header(f"TESTING KEY: {key[:5]}...{key[-4:]}")
        
        # Try different authentication methods
        auth_methods = [
            test_mem0_auth_method1,
            test_mem0_auth_method2,
            test_mem0_auth_method3,
            test_mem0_auth_method4
        ]
        
        success = False
        for method in auth_methods:
            if method(key):
                success = True
                print_success(f"Authentication successful with method {method.__name__}")
                break
        
        if not success:
            print_warning("All standard authentication methods failed, trying alternative endpoints...")
            alt_success, endpoint, headers = test_mem0_alternative_endpoints(key)
            
            if alt_success:
                print_success(f"Found working endpoint: {endpoint}")
                print_success(f"With headers: {headers}")
                success = True
        
        if success:
            print_success(f"Found working authentication method for key {key[:5]}...{key[-4:]}")
            return 0
    
    print_error("All authentication methods failed for all keys")
    return 1

if __name__ == "__main__":
    sys.exit(main())

