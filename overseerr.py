# Usage:
# python3 ./overseerr.py --api_key MT............== --overseerr_url http://localhost:5055

import requests
import argparse
import json
from collections import namedtuple

Request = namedtuple('Request', ['id', 'type', 'status', 'media_id', 'media_type', 'requested_by'])

import json

class ConfigManager:
    def __init__(self, config_path):
        self.config_path = config_path

    def load(self):
        """Reads the configuration file and returns the last seen request ID."""
        try:
            with open(self.config_path, 'r') as file:
                config = json.load(file)
                return config.get('last_seen_request', -1)
        except (FileNotFoundError, json.JSONDecodeError):
            return -1

    def update(self, last_seen_request):
        """Updates the configuration file with the last seen request ID."""
        with open(self.config_path, 'w') as file:
            json.dump({'last_seen_request': last_seen_request}, file)

def get_overseerr_requests(api_key, overseerr_url, last_seen_request):
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
            for request in data['results'] if request['id'] > last_seen_request
        ]
        return requests_list

    except requests.RequestException as e:
        print(f"Error fetching data from Overseerr: {e}")
        return []

def parse_args():
    parser = argparse.ArgumentParser(description='Fetches requested items from Overseerr.')
    parser.add_argument('--api_key', type=str, help='API Key for Overseerr')
    parser.add_argument('--overseerr_url', type=str, help='URL of the Overseerr instance')
    parser.add_argument('--config', type=str, help='Path to the configuration file')

    args = parser.parse_args()
    return args

def main():
    args = parse_args()
    config_manager = ConfigManager(args.config)

    last_seen_request = config_manager.load()
    new_requests = get_overseerr_requests(args.api_key, args.overseerr_url, last_seen_request)
    
    if new_requests:
        print(new_requests)
        last_request_id = new_requests[-1].id
        config_manager.update(last_request_id)
    else:
        print("No new requests.")

if __name__ == "__main__":
    main()
