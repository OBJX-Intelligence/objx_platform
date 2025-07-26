#!/usr/bin/env python3
"""
OBJX Platform - MEM0 API Key Test Script
Tests MEM0 API keys to find a working one
"""

import os
import sys
import json
import time
import requests

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

def test_mem0_key(api_key, key_name=""):
    """Test a MEM0 API key"""
    print_header(f"TESTING MEM0 API KEY: {key_name}")
    
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
            "content": f"This is a test memory from OBJX Platform using key {key_name}",
            "metadata": {
                "source": "OBJX Platform Test",
                "timestamp": time.time()
            }
        }
        
        print_info("Attempting to create a test memory...")
        create_response = requests.post(create_url, headers=headers, json=create_payload)
        
        if create_response.status_code == 200 or create_response.status_code == 201:
            memory_id = create_response.json().get("id")
            print_success(f"Successfully created test memory with ID: {memory_id}")
            
            # Test retrieving the memory
            get_url = f"https://api.mem0.ai/v1/memories/{memory_id}"
            print_info("Attempting to retrieve the test memory...")
            get_response = requests.get(get_url, headers=headers)
            
            if get_response.status_code == 200:
                print_success(f"Successfully retrieved test memory")
                
                # Test deleting the memory
                delete_url = f"https://api.mem0.ai/v1/memories/{memory_id}"
                print_info("Attempting to delete the test memory...")
                delete_response = requests.delete(delete_url, headers=headers)
                
                if delete_response.status_code == 200 or delete_response.status_code == 204:
                    print_success(f"Successfully deleted test memory")
                    return True, "All operations successful"
                else:
                    print_warning(f"Failed to delete test memory: {delete_response.status_code}")
                    print_info(f"Response: {delete_response.text}")
                    return True, "Create and retrieve successful, but delete failed"
            else:
                print_warning(f"Failed to retrieve test memory: {get_response.status_code}")
                print_info(f"Response: {get_response.text}")
                return False, f"Failed to retrieve memory: {get_response.status_code}"
        else:
            print_error(f"Failed to create test memory: {create_response.status_code}")
            print_info(f"Response: {create_response.text}")
            return False, f"Failed to create memory: {create_response.status_code}"
    except Exception as e:
        print_error(f"Failed to connect to MEM0 API: {str(e)}")
        return False, str(e)

def main():
    """Main function to test MEM0 API keys"""
    print_header("OBJX PLATFORM - MEM0 API KEY TESTS")
    
    # Test keys
    keys = [
        ("m0-NYHyffT0aUwQUxxP8yleXWMcob6y1WkeBscMb2UH", "Key 1"),
        ("m0-iL5CB1HAi2fONORs9JialJXrS1xZfXS0HATj3W7i", "Key 2")
    ]
    
    results = {}
    working_key = None
    
    for key, name in keys:
        success, message = test_mem0_key(key, name)
        results[name] = {
            "key": key,
            "success": success,
            "message": message
        }
        
        if success and working_key is None:
            working_key = key
    
    print_header("TEST RESULTS SUMMARY")
    
    for name, result in results.items():
        if result["success"]:
            print_success(f"{name}: Working ({result['message']})")
        else:
            print_error(f"{name}: Failed ({result['message']})")
    
    if working_key:
        print_success(f"\nFound working MEM0 API key: {working_key[:5]}...{working_key[-4:]}")
        print_info("You can use this key in your .env file")
        
        # Update the .env file with the working key
        env_file = "../.env"
        if os.path.exists(env_file):
            try:
                with open(env_file, 'r') as f:
                    env_content = f.read()
                
                # Replace the MEM0 API key
                if "MEM0_API_KEY=" in env_content:
                    new_content = ""
                    for line in env_content.split('\n'):
                        if line.startswith("MEM0_API_KEY="):
                            new_content += f"MEM0_API_KEY={working_key}\n"
                        else:
                            new_content += line + "\n"
                    
                    with open(env_file, 'w') as f:
                        f.write(new_content)
                    
                    print_success(f"Updated .env file with working MEM0 API key")
            except Exception as e:
                print_error(f"Failed to update .env file: {str(e)}")
        
        return 0
    else:
        print_warning("\nNo working MEM0 API key found. Using local memory fallback.")
        return 1

if __name__ == "__main__":
    sys.exit(main())

