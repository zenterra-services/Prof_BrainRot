#!/usr/bin/env python3
"""
Check the status of the Wan 2.5 task we just created
"""

import requests


API_KEY = "sk-c3ba3cd1903c419bb24b7970ecd01856"
TASK_ID = "d5e66832-eade-4488-a5e6-f5cb81d457e4"


def check_task_status():
    print(f"Checking status for task: {TASK_ID}")

    try:
        response = requests.get(
            f"https://dashscope-intl.aliyuncs.com/api/v1/tasks/{TASK_ID}",
            headers={"Authorization": f"Bearer {API_KEY}"}
        )

        if response.status_code == 200:
            result = response.json()
            print(f"Response: {json.dumps(result, indent=2)}")

            task_status = result.get("output", {}).get("task_status")
            print(f"\nTask Status: {task_status}")

            if task_status == "SUCCEEDED":
                video_url = result.get("output", {}).get("video_url")
                print(f"✅ Video ready! URL: {video_url}")
                print(f"Duration: {result.get('output', {}).get('duration')} seconds")
                return True
            elif task_status == "FAILED":
                error_code = result.get("output", {}).get("code")
                error_message = result.get("output", {}).get("message")
                print(f"❌ Task failed: {error_code} - {error_message}")
                return False
            else:
                print(f"⏳ Task is {task_status}")
                return False
        else:
            print(f"❌ Status check failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False

    except Exception as e:
        print(f"❌ Error checking status: {e}")
        return False


if __name__ == "__main__":
    import json

    print("=" * 50)
    print("Wan 2.5 Task Status Check")
    print("=" * 50)

    check_task_status()

    print("\n" + "=" * 50)
    print("If status is PENDING/RUNNING, the task is processing normally.")
    print("Check again in 30-60 seconds for completion.")
    print("=" * 50)
