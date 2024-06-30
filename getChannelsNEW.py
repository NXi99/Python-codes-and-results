import requests
import json


def get_channels_by_pubkey(pubkey):
    index = 0  # start index at 0
    all_channels = []
    while True:
        url = f"https://mempool.space/api/v1/lightning/channels?public_key={pubkey}&status=open&index={index}"
        try:
            response = requests.get(url, timeout=20)
            response.raise_for_status()
            channels = response.json()
            if not channels:  # If no more channels, break the loop
                break
            all_channels.extend(channels)
            index += len(channels)  # update index to fetch next set of channels
        except requests.exceptions.Timeout:
            print(f"Timeout occurred while fetching channels data for {pubkey}")
            continue  # retry fetching the same batch
        except requests.exceptions.RequestException as e:
            print(f"An error occurred while fetching channels data for {pubkey}: {e}")
            break  # exit on other errors
    return all_channels


# Load the high connectivity nodes data
with open('high_connectivity_nodes.json', 'r') as file:
    high_conn_nodes = json.load(file)

all_channels_data = {}

# Iterate over each high connectivity node
for node in high_conn_nodes:
    pubkey = node['public_key']
    print(f"Fetching channel data for public key: {pubkey}")
    channels = get_channels_by_pubkey(pubkey)
    all_channels_data[pubkey] = channels
    print(f"Collected {len(channels)} channels for {pubkey}")

# Save the collected channel data
with open("channels_detailed.json", "w") as f:
    json.dump(all_channels_data, f)
