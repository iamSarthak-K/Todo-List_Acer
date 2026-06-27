import requests
import json

BASE_URL = "http://localhost:8000"

def run_tests():
    print("Testing AI Layer Endpoints...\n")

    # 1. Login to get JWT token
    print("1. Logging in via /auth/demo-login...")
    login_resp = requests.post(f"{BASE_URL}/auth/demo-login")
    if login_resp.status_code != 200:
        print(f"Failed to login: {login_resp.text}")
        return
    token = login_resp.json().get("access_token")
    headers = {"Authorization": f"Bearer {token}"}
    print("   -> Successfully acquired token.\n")

    # 2. Test Chat Agent
    print("2. Testing Chat Agent (/api/ai/chat)...")
    chat_payload = {
        "message": "I feel overwhelmed with my work today.",
        "history": []
    }
    chat_resp = requests.post(f"{BASE_URL}/api/ai/chat", json=chat_payload, headers=headers)
    if chat_resp.status_code == 200:
        print("   -> Response:", json.dumps(chat_resp.json(), indent=2))
    else:
        print(f"   -> Failed: {chat_resp.text}")
    print()

    # 3. Test Extract Commitment Agent
    print("3. Testing Extract Agent (/api/ai/extract)...")
    extract_payload = {
        "text": "I need to finish the marketing report by next Friday."
    }
    extract_resp = requests.post(f"{BASE_URL}/api/ai/extract", json=extract_payload, headers=headers)
    if extract_resp.status_code == 200:
        print("   -> Response:", json.dumps(extract_resp.json(), indent=2))
    else:
        print(f"   -> Failed: {extract_resp.text}")
    print()

    # 4. Test Planner Agent
    print("4. Testing Planner Agent (/api/ai/plan)...")
    plan_payload = {
        "commitment_id": 1 # Note: Ensure commitment ID 1 exists, or it just mocks context
    }
    plan_resp = requests.post(f"{BASE_URL}/api/ai/plan", json=plan_payload, headers=headers)
    if plan_resp.status_code == 200:
        print("   -> Response:", json.dumps(plan_resp.json(), indent=2))
    else:
        print(f"   -> Failed: {plan_resp.text}")
    print()

    # 5. Test Recovery Agent
    print("5. Testing Recovery Agent (/api/ai/recover)...")
    recover_payload = {
        "task_id": 1
    }
    recover_resp = requests.post(f"{BASE_URL}/api/ai/recover", json=recover_payload, headers=headers)
    if recover_resp.status_code == 200:
        print("   -> Response:", json.dumps(recover_resp.json(), indent=2))
    else:
        print(f"   -> Failed: {recover_resp.text}")
    print()

if __name__ == "__main__":
    try:
        # Check if server is up
        health = requests.get(f"{BASE_URL}/health")
        if health.status_code == 200:
            run_tests()
        else:
            print("Server is not healthy.")
    except requests.exceptions.ConnectionError:
        print("Cannot connect to the backend server. Please make sure uvicorn is running on port 8000 (e.g., cd backend && uvicorn app.main:app --reload)")
