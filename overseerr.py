import requests
import argparse

def get_overseerr_requests(api_key, overseerr_url):
    """Fetches requested items from Overseerr."""
    headers = {
        "X-Api-Key": api_key,
    }

    try:
        response = requests.get(f"{overseerr_url}/api/v1/request", headers=headers)
        response.raise_for_status()
        print(response.text)

        # Assuming the data is in JSON format and contains a list of requests
        requests_data = response.json()
        for request in requests_data:
            print(f"Requested Item: {request['title']} by {request['requestedBy']}")

    except requests.RequestException as e:
        print(f"Error fetching data from Overseerr: {e}")


def  parse_args():
    parser = argparse.ArgumentParser(description='Fetches requested items from Overseerr.')
    parser.add_argument('--api_key', type=str, help='API Key for Overseerr')
    parser.add_argument('--overseerr_url', type=str, help='URL of the Overseerr instance')

    args = parser.parse_args()

    return args

def main():
    args = parse_args()
    get_overseerr_requests(args.api_key, args.overseerr_url)

if __name__ == "__main__":
    main()
