import urllib3
import json

def main():
    print("Hello from pyconsole with urllib3!")
    print("Making HTTP request to JSONPlaceholder API...")

    try:
        # Create HTTP connection pool manager
        http = urllib3.PoolManager()

        # Make GET request to a test API
        url = "https://jsonplaceholder.typicode.com/posts/1"
        response = http.request('GET', url)

        # Parse and display response
        if response.status == 200:
            data = json.loads(response.data.decode('utf-8'))
            print(f"\nAPI Response (Status: {response.status}):")
            print(f"Title: {data.get('title', 'N/A')}")
            print(f"Body: {data.get('body', 'N/A')[:100]}...")
        else:
            print(f"Request failed with status: {response.status}")

    except Exception as e:
        print(f"Error making HTTP request: {e}")

    print("\nPress Enter to exit...")
    input()  # Keep console window open until user presses Enter


if __name__ == "__main__":
    main()
