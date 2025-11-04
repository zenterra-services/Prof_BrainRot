#!/usr/bin/env python3
"""
Test script for Wan 2.5 API integration
Verifies API key validity and basic functionality
"""

import requests
import time
from datetime import datetime

# Wan 2.5 API Configuration
API_KEY = "sk-c3ba3cd1903c419bb24b7970ecd01856"
BASE_URL = "https://dashscope-intl.aliyuncs.com/api/v1/services/aigc/video-generation"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "X-DashScope-Async": "enable"
}


def test_api_key_validity():
    """Test if the API key is valid and account is active"""
    print("🧪 Testing Wan 2.5 API Key Validity...")

    try:
        # Test user info endpoint
        response = requests.get(
            "https://dashscope-intl.aliyuncs.com/api/v1/users/me",
            headers={"Authorization": f"Bearer {API_KEY}"}
        )

        if response.status_code == 200:
            user_data = response.json()
            print("✅ API Key is valid!")
            print(f"   User ID: {user_data.get('user_id', 'N/A')}")
            print(f"   Account Status: {user_data.get('status', 'N/A')}")
            return True
        else:
            print(f"❌ API Key test failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False

    except Exception as e:
        print(f"❌ API connection error: {e}")
        return False


def test_video_generation():
    """Test actual video generation with educational content"""
    print("\n🎥 Testing Video Generation...")

    # Sample educational content
    test_prompt = "A friendly teacher explaining basic algebra concepts with colorful animations and clear visual examples. The scene shows mathematical equations floating in space with animated arrows and highlights."

    request_data = {
        "model": "wan2.5-t2v-preview",
        "input": {
            "prompt": test_prompt,
            "negative_prompt": "blurry, low quality, distracting elements, watermark, logo, text overlay, shaky camera, poor lighting, inappropriate content"
        },
        "parameters": {
            "size": "1280*720",
            "duration": 10,
            "audio": True,
            "prompt_extend": True,
            "watermark": False,
            "seed": 12345
        }
    }

    try:
        # Submit video generation task
        print("   Submitting task...")
        response = requests.post(
            f"{BASE_URL}/video-synthesis",
            headers=HEADERS,
            json=request_data
        )

        if response.status_code == 201:
            result = response.json()
            task_id = result.get("output", {}).get("task_id")
            print("✅ Task submitted successfully!")
            print(f"   Task ID: {task_id}")
            print(f"   Status: {result.get('output', {}).get('task_status')}")

            # Poll for completion
            print("   Polling for completion...")
            return poll_task_status(task_id)
        else:
            print(f"❌ Task submission failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False

    except Exception as e:
        print(f"❌ Video generation error: {e}")
        return False


def poll_task_status(task_id, max_attempts=10, interval=30):
    """Poll task status until completion or timeout"""

    for attempt in range(max_attempts):
        try:
            response = requests.get(
                f"https://dashscope-intl.aliyuncs.com/api/v1/tasks/{task_id}",
                headers={"Authorization": f"Bearer {API_KEY}"}
            )

            if response.status_code == 200:
                result = response.json()
                task_status = result.get("output", {}).get("task_status")

                print(f"   Attempt {attempt + 1}: Status = {task_status}")

                if task_status == "SUCCEEDED":
                    video_url = result.get("output", {}).get("video_url")
                    print("✅ Video generation completed!")
                    print(f"   Video URL: {video_url}")
                    print(
                        f"   Duration: {result.get('output', {}).get('duration', 'N/A')} seconds")
                    return True
                elif task_status == "FAILED":
                    error_code = result.get("output", {}).get("code")
                    error_message = result.get("output", {}).get("message")
                    print(f"❌ Video generation failed: {error_code} - {error_message}")
                    return False
                elif task_status in ["PENDING", "RUNNING"]:
                    if attempt < max_attempts - 1:
                        print(f"   Waiting {interval} seconds...")
                        time.sleep(interval)
                    continue
                else:
                    print(f"❌ Unknown status: {task_status}")
                    return False
            else:
                print(f"❌ Status check failed: {response.status_code}")
                return False

        except Exception as e:
            print(f"❌ Status check error: {e}")
            return False

    print(f"❌ Timeout after {max_attempts} attempts")
    return False


def test_rate_limits():
    """Test API rate limits"""
    print("\n⚡ Testing Rate Limits...")

    # Make multiple quick requests to test limits
    for i in range(3):
        try:
            response = requests.get(
                "https://dashscope-intl.aliyuncs.com/api/v1/users/me",
                headers={"Authorization": f"Bearer {API_KEY}"}
            )

            if response.status_code == 200:
                print(f"   Request {i + 1}: ✅ Success")
            elif response.status_code == 429:
                print(f"   Request {i + 1}: ⚠️ Rate limited")
                break
            else:
                print(f"   Request {i + 1}: ❌ Failed ({response.status_code})")

            time.sleep(1)  # Small delay between requests

        except Exception as e:
            print(f"   Request {i + 1}: ❌ Error - {e}")


def main():
    """Main test function"""
    print("=" * 60)
    print("🚀 Wan 2.5 API Integration Test")
    print("=" * 60)
    print(f"API Key: {API_KEY[:10]}...")
    print(f"Base URL: {BASE_URL}")
    print(f"Test Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # Run tests
    api_valid = test_api_key_validity()

    if api_valid:
        test_rate_limits()
        video_success = test_video_generation()

        print("\n" + "=" * 60)
        print("📊 Test Results Summary")
        print("=" * 60)
        print("✅ API Key Validity: PASS")
        print(
            f"{'✅' if video_success else '❌'} Video Generation: {'PASS' if video_success else 'FAIL'}")

        if video_success:
            print("\n🎉 Wan 2.5 API is ready for integration!")
            print("   You can now use this API key in your ProfBrainRot setup.")
        else:
            print("\n⚠️  Video generation failed, but API key is valid.")
            print("   Check the error messages above for troubleshooting.")
    else:
        print("\n❌ API key validation failed.")
        print("   Please check your API key and ensure billing is enabled.")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
