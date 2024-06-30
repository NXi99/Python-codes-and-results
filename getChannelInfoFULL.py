import concurrent
import requests
import json
from concurrent.futures import ThreadPoolExecutor


def get_channel_data(channel_id):
    url = f"https://mempool.space/api/v1/lightning/channels/{channel_id}"
    try:
        response = requests.get(url, timeout=20)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        print(f"Timeout occurred; retrying for channel: {channel_id}")
        return get_channel_data(channel_id)  # Retry fetching on timeout
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for channel {channel_id}: {e}")
        return None


def load_data():
    with open('channels_detailed.json', 'r') as file:
        return json.load(file)


def save_data(data):
    with open("channels_full.json", "w") as f:
        json.dump(data, f)


def main():
    data = load_data()
    unique_channel_ids = set(channel['id'] for channels in data.values() for channel in channels)

    channel_data_to_save = {}

    with ThreadPoolExecutor(max_workers=50) as executor:  # Adjust max_workers as per your system capability
        future_to_channel = {executor.submit(get_channel_data, channel_id): channel_id for channel_id in
                             unique_channel_ids}
        for future in concurrent.futures.as_completed(future_to_channel):
            channel_id = future_to_channel[future]
            try:
                info = future.result()
                if info:
                    channel_data_to_save[channel_id] = info
                    print(f"Data collected for channel {channel_id}")
            except Exception as e:
                print(f"Exception occurred for channel {channel_id}: {e}")

    save_data(channel_data_to_save)
    print("Data collection complete and saved.")


if __name__ == "__main__":
    main()
