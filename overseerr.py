# Usage:
# python3 ./overseerr.py --api_key MT............== --overseerr_url http://localhost:5055

import requests
import argparse
from collections import namedtuple

Request = namedtuple('Request', ['id', 'type', 'status', 'media_id', 'media_type', 'requested_by'])


def get_overseerr_requests(api_key, overseerr_url):
    """Fetches requested items from Overseerr and returns them as a list of named tuples."""
    headers = {"X-Api-Key": api_key}

    try:
        response = requests.get(f"{overseerr_url}/api/v1/request", headers=headers)
        response.raise_for_status()

        data = response.json()
        requests_list = [
            Request(
                id=request['id'],
                type=request['type'],
                status=request['status'],
                media_id=request['media']['id'],
                media_type=request['media']['mediaType'],
                requested_by=request['requestedBy']['plexUsername']
            )
            for request in data['results']
        ]
        return requests_list

    except requests.RequestException as e:
        print(f"Error fetching data from Overseerr: {e}")
        return []


def  parse_args():
    parser = argparse.ArgumentParser(description='Fetches requested items from Overseerr.')
    parser.add_argument('--api_key', type=str, help='API Key for Overseerr')
    parser.add_argument('--overseerr_url', type=str, help='URL of the Overseerr instance')

    args = parser.parse_args()

    return args

def main():
    args = parse_args()
    requests = get_overseerr_requests(args.api_key, args.overseerr_url)
    print(requests)

if __name__ == "__main__":
    main()
