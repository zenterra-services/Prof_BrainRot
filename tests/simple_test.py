#!/usr/bin/env python3
"""
Simple test to verify Wan 2.5 API is working without full system setup
"""

import requests


def test_wan25_simple():
    """Simple test with minimal setup"""
    print("Testing Wan 2.5 API with simple educational content...")

    API_KEY = "sk-c3ba3cd1903c419bb24b7970ecd01856"

    # Simple educational prompt
    prompt = "A teacher explaining fractions with visual examples and clear animations"

    request_data = {
        "model": "wan2.5-t2v-preview",
        "input": {
            "prompt": prompt,
            "negative_prompt": "blurry, low quality, watermark, text"
        },
        "parameters": {
            "size": "1280*720",
            "duration": 5,
            "audio": True,
            "watermark": False
        }
    }

    try:
        print("Submitting task...")
        response = requests.post(
            "https://dashscope-intl.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json",
                "X-DashScope-Async": "enable"
            },
            json=request_data
        )

        print(f"Status: {response.status_code}")

        if response.status_code == 201:
            result = response.json()
            task_id = result.get("output", {}).get("task_id")
            print(f"SUCCESS! Task created: {task_id}")
            print(f"Status: {result.get('output', {}).get('task_status')}")
            return True
        else:
            print(f"Failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False

    except Exception as e:
        print(f"Error: {e}")
        return False


if __name__ == "__main__":
    print("=" * 50)
    print("SIMPLE WAN 2.5 API TEST")
    print("=" * 50)

    success = test_wan25_simple()

    if success:
        print("\n✓ Wan 2.5 API is working correctly!")
        print("✓ Your API key is valid!")
        print("✓ Ready for full system setup!")
    else:
        print("\n✗ API test failed")
        print("Check your API key and internet connection")

    print("\n" + "=" * 50)
