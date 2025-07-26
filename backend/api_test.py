#!/usr/bin/env python3
"""
OBJX Platform - API Connection Test Script
Tests connections to OpenAI, Anthropic, and MEM0 APIs with provided keys
"""

import os
import sys
import json
import time
from dotenv import load_dotenv
import requests
from openai import OpenAI
import anthropic

# Load environment variables
load_dotenv()

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

def test_openai_connection():
    """Test connection to OpenAI API"""
    print_header("TESTING OPENAI API CONNECTION")
    
    api_key = os.getenv("OPENAI_API_KEY")
    model = os.getenv("OBJX_OPENAI_MODEL", "gpt-4.1-mini")
    
    if not api_key:
        print_error("OpenAI API key not found in environment variables")
        return False
    
    print_info(f"Using model: {model}")
    print_info(f"API Key: {api_key[:5]}...{api_key[-4:]}")
    
    try:
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Test connection to OpenAI API. Respond with 'Connection successful!'"}
            ],
            max_tokens=50
        )
        
        print_success(f"Connection successful!")
        print_info(f"Response: {response.choices[0].message.content}")
        return True
    except Exception as e:
        print_error(f"Failed to connect to OpenAI API: {str(e)}")
        return False

def test_anthropic_connection():
    """Test connection to Anthropic API"""
    print_header("TESTING ANTHROPIC API CONNECTION")
    
    api_key = os.getenv("ANTHROPIC_API_KEY")
    model = os.getenv("OBJX_ANTHROPIC_MODEL", "claude-sonnet-4-20250514")
    
    if not api_key:
        print_error("Anthropic API key not found in environment variables")
        return False
    
    print_info(f"Using model: {model}")
    print_info(f"API Key: {api_key[:5]}...{api_key[-4:]}")
    
    try:
        client = anthropic.Anthropic(api_key=api_key)
        response = client.messages.create(
            model=model,
            max_tokens=50,
            messages=[
                {"role": "user", "content": "Test connection to Anthropic API. Respond with 'Connection successful!'"}
            ]
        )
        
        print_success(f"Connection successful!")
        print_info(f"Response: {response.content[0].text}")
        return True
    except Exception as e:
        print_error(f"Failed to connect to Anthropic API: {str(e)}")
        return False

def test_mem0_connection():
    """Test connection to MEM0 API"""
    print_header("TESTING MEM0 API CONNECTION")
    
    api_key = os.getenv("MEM0_API_KEY")
    
    if not api_key:
        print_error("MEM0 API key not found in environment variables")
        return False
    
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
            "content": "This is a test memory from OBJX Platform",
            "metadata": {
                "source": "OBJX Platform Test",
                "timestamp": time.time()
            }
        }
        
        create_response = requests.post(create_url, headers=headers, json=create_payload)
        
        if create_response.status_code == 200 or create_response.status_code == 201:
            memory_id = create_response.json().get("id")
            print_success(f"Successfully created test memory with ID: {memory_id}")
            
            # Test retrieving the memory
            get_url = f"https://api.mem0.ai/v1/memories/{memory_id}"
            get_response = requests.get(get_url, headers=headers)
            
            if get_response.status_code == 200:
                print_success(f"Successfully retrieved test memory")
                
                # Test deleting the memory
                delete_url = f"https://api.mem0.ai/v1/memories/{memory_id}"
                delete_response = requests.delete(delete_url, headers=headers)
                
                if delete_response.status_code == 200 or delete_response.status_code == 204:
                    print_success(f"Successfully deleted test memory")
                    return True
                else:
                    print_warning(f"Failed to delete test memory: {delete_response.status_code}")
                    print_info(f"Response: {delete_response.text}")
                    return True  # Still return True as we successfully created and retrieved
            else:
                print_warning(f"Failed to retrieve test memory: {get_response.status_code}")
                print_info(f"Response: {get_response.text}")
                return False
        else:
            print_error(f"Failed to create test memory: {create_response.status_code}")
            print_info(f"Response: {create_response.text}")
            return False
    except Exception as e:
        print_error(f"Failed to connect to MEM0 API: {str(e)}")
        return False

def main():
    """Main function to run all tests"""
    print_header("OBJX PLATFORM - API CONNECTION TESTS")
    
    results = {
        "openai": test_openai_connection(),
        "anthropic": test_anthropic_connection(),
        "mem0": test_mem0_connection()
    }
    
    print_header("TEST RESULTS SUMMARY")
    
    for api, success in results.items():
        if success:
            print_success(f"{api.upper()} API: Connection successful")
        else:
            print_error(f"{api.upper()} API: Connection failed")
    
    if all(results.values()):
        print_success("\nAll API connections successful! The OBJX Platform is ready to use.")
        return 0
    else:
        print_warning("\nSome API connections failed. Please check the error messages above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())

