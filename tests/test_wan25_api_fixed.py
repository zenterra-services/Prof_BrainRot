#!/usr/bin/env python3
"""
Test script for Wan 2.5 API integration - Fixed endpoint version
"""

import requests
from datetime import datetime

# Force UTF-8 encoding for Windows
import sys
sys.stdout.reconfigure(encoding='utf-8')

# Wan 2.5 API Configuration
API_KEY = "sk-c3ba3cd1903c419bb24b7970ecd01856"
BASE_URL = "https://dashscope-intl.aliyuncs.com/api/v1/services/aigc/video-generation"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "X-DashScope-Async": "enable"
}


def test_api_key_basic():
    """Test basic API key functionality with a simple task submission"""
    print("Testing Wan 2.5 API Key with task submission...")

    # Simple test prompt
    test_prompt = "A simple educational animation showing basic math concepts with colorful visuals"

    request_data = {
        "model": "wan2.5-t2v-preview",
        "input": {
            "prompt": test_prompt,
            "negative_prompt": "blurry, low quality, watermark"
        },
        "parameters": {
            "size": "1280*720",
            "duration": 5,  # Shorter duration for testing
            "audio": True,
            "prompt_extend": True,
            "watermark": False,
            "seed": 12345
        }
    }

    try:
        print("   Submitting test task...")
        response = requests.post(
            f"{BASE_URL}/video-synthesis",
            headers=HEADERS,
            json=request_data
        )

        print(f"   Response Status: {response.status_code}")
        print(f"   Response Headers: {dict(response.headers)}")

        if response.status_code == 201:
            result = response.json()
            print("✓ Task submitted successfully!")
            print(f"   Task ID: {result.get('output', {}).get('task_id')}")
            print(f"   Status: {result.get('output', {}).get('task_status')}")

            # Save the task ID for status checking
            task_id = result.get('output', {}).get('task_id')
            if task_id:
                return check_task_status(task_id)
            return True
        elif response.status_code == 401:
            print("✗ Authentication failed - API key may be invalid")
            return False
        elif response.status_code == 403:
            print("✗ Access forbidden - check billing/account status")
            return False
        elif response.status_code == 429:
            print("✗ Rate limit exceeded")
            return False
        else:
            print(f"✗ Task submission failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False

    except requests.exceptions.RequestException as e:
        print(f"✗ Network error: {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False


def check_task_status(task_id):
    """Check the status of a submitted task"""
    print(f"\n   Checking status for task: {task_id}")

    try:
        response = requests.get(
            f"https://dashscope-intl.aliyuncs.com/api/v1/tasks/{task_id}",
            headers={"Authorization": f"Bearer {API_KEY}"}
        )

        if response.status_code == 200:
            result = response.json()
            task_status = result.get("output", {}).get("task_status")
            print(f"   Current Status: {task_status}")

            if task_status == "SUCCEEDED":
                video_url = result.get("output", {}).get("video_url")
                print("✓ Task completed successfully!")
                print(f"   Video URL: {video_url}")
                return True
            elif task_status == "FAILED":
                error_code = result.get("output", {}).get("code")
                error_message = result.get("output", {}).get("message")
                print(f"✗ Task failed: {error_code} - {error_message}")
                return False
            else:
                print(f"   Task is {task_status}")
                return True  # API is working, task is processing
        else:
            print(f"✗ Status check failed: {response.status_code}")
            return False

    except Exception as e:
        print(f"✗ Status check error: {e}")
        return False


def test_direct_endpoint():
    """Test direct connection to the API endpoint"""
    print("\nTesting direct API endpoint connection...")

    try:
        # Test the base URL
        response = requests.get(
            "https://dashscope-intl.aliyuncs.com/api/v1/services",
            headers={"Authorization": f"Bearer {API_KEY}"}
        )

        print(f"   Base URL test: {response.status_code}")

        # Test models endpoint
        response = requests.get(
            "https://dashscope-intl.aliyuncs.com/api/v1/models",
            headers={"Authorization": f"Bearer {API_KEY}"}
        )

        print(f"   Models endpoint test: {response.status_code}")

        if response.status_code == 200:
            models = response.json()
            wan_models = [m for m in models.get(
                'models', []) if 'wan' in m.get('id', '').lower()]
            if wan_models:
                print(f"   Found Wan models: {[m['id'] for m in wan_models]}")
                return True

        return False

    except Exception as e:
        print(f"✗ Endpoint test error: {e}")
        return False


def main():
    """Main test function"""
    print("=" * 60)
    print("Wan 2.5 API Integration Test")
    print("=" * 60)
    print(f"API Key: {API_KEY[:10]}...")
    print(f"Test Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # Run tests
    print("1. Testing direct endpoints...")
    endpoint_test = test_direct_endpoint()

    print("\n2. Testing video generation...")
    video_test = test_api_key_basic()

    print("\n" + "=" * 60)
    print("Test Results Summary")
    print("=" * 60)
    print(f"{'✓' if endpoint_test else '✗'} Direct Endpoint Test: {'PASS' if endpoint_te
                                                                   st else 'FAIL'}")
    print(f"{'✓' if video_test else '✗'} Video Generation Test: {'PASS' if video_test el
                                                                 se 'FAIL'}")

    if video_test:
        print("\n🎉 Wan 2.5 API is ready for integration!")
        print("   You can now use this API key in your ProfBrainRot setup.")
        print("   Estimated cost: $0.10 per 10-second video")
    else:
        print("\n⚠ Video generation had issues, but API may still work.")
        print("   Check the error messages above for troubleshooting.")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
