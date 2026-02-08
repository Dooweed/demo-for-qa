
import requests

def test_patch_without_slash():
    url = "http://localhost:8000/api/authors/1"
    print(f"Testing PATCH {url}")
    # We expect this to return 401 if unauthenticated, 
    # but based on the issue description, it might return 200 with unchanged object.
    try:
        response = requests.patch(url, data={"first_name": "New Name"})
        print(f"Status Code: {response.status_code}")
        print(f"Response Body: {response.text}")
        if response.history:
            print("Redirect history:")
            for resp in response.history:
                print(f"  {resp.status_code} to {resp.headers.get('Location')}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_patch_without_slash()
